from typing import List, Tuple, Optional, Dict, Any, Callable
import tempfile
import logging

from fastapi import FastAPI, UploadFile, APIRouter, Response, Request
from fastapi.responses import FileResponse
from fastapi.routing import APIRoute
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse
from pydantic import BaseModel, Field
import pygambit as gbt
import numpy as np
import uvicorn


def log_info(request_body, response_body):
    logging.info(f"Request body: {request_body}")
    logging.info(f"Response body: {response_body}")


class LoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request_body = await request.body()
            response = await original_route_handler(request)
            logging.info(f"Request body: {request_body}")
            logging.info(f"Response body: {response.body}")
            if isinstance(response, StreamingResponse):
                res_body = b''
                async for item in response.body_iterator:
                    res_body += item

                task = BackgroundTask(log_info, request_body, res_body)
                return Response(content=res_body, status_code=response.status_code,
                                headers=dict(response.headers), media_type=response.media_type, background=task)
            else:
                res_body = response.body
                logging.info(f"Request body: {request_body}")
                logging.info(f"Response body: {res_body}")
                return response

        return custom_route_handler


app = FastAPI(debug=True)
router = APIRouter(route_class=LoggingRoute)
logging.basicConfig(level=logging.DEBUG)


class AnalysisData(BaseModel):
    p1_probs: List[Tuple[int, int]]
    p2_probs: List[Tuple[int, int]]
    payoff: Tuple[int, int]

    @classmethod
    def analyze(cls, game: gbt.Game) -> "AnalysisData":
        """Analyze the game and set the mixed strategy probabilities"""

        solver = gbt.nash.lp_solve
        eqa = solver(game)
        analysisData = AnalysisData(
            p1_probs=[eqa[0].strategy_value(
                strategy).as_integer_ratio() for strategy in game.players[0].strategies],
            p2_probs=[eqa[0].strategy_value(
                strategy).as_integer_ratio() for strategy in game.players[1].strategies],
            payoff=eqa[0].payoff(game.players[0]).as_integer_ratio()
        )
        return analysisData


class MixupData(BaseModel):
    title: str = Field(default="Untitled strategic game")
    comment: str = Field(default="")
    player_1: str = Field(default="1")
    player_2: str = Field(default="2")
    p1_strategies: List[str] = None
    p2_strategies: List[str] = None
    rows: int
    cols: int
    matrix: List[List[int]]

    @classmethod
    def from_gbt(cls, game: gbt.Game) -> "MixupData":
        """Create the form data from a Pygambit game"""

        rows = len(game.players[0].strategies)
        cols = len(game.players[1].strategies)
        matrix = [[0 for _ in range(cols)] for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                value = game.outcomes[i * cols + j][game.players[0]].numerator
                matrix[i][j] = value

        mixupData = MixupData(
            title=game.title,
            comment=game.comment,
            player_1=game.players[0].label,
            player_2=game.players[1].label,
            p1_strategies=[s.label for s in game.players[0].strategies],
            p2_strategies=[s.label for s in game.players[1].strategies],
            rows=rows,
            cols=cols,
            matrix=matrix
        )

        return mixupData

    def to_gbt(self) -> gbt.Game:
        """Converts the form data to a pygambit game"""

        payoff_matrix = np.array(self.matrix)
        game = gbt.Game.from_arrays(
            payoff_matrix, -payoff_matrix, title=self.title)

        game.players[0].label = self.player_1
        game.players[1].label = self.player_2

        for label, strategy in zip(self.p1_strategies, game.players[0].strategies):
            strategy.label = label
        for label, strategy in zip(self.p2_strategies, game.players[1].strategies):
            strategy.label = label

        game.comment = self.comment
        return game


@router.post("/analyze")
def analyze_game(mixupData: MixupData):
    """Receive a game and return the analysis"""

    game = mixupData.to_gbt()
    analysis = AnalysisData.analyze(game)
    return analysis.model_dump()


@app.post("/download")
def download_game(mixupData: MixupData):
    """Receive a game and return the NFG file with analysis"""

    game = mixupData.to_gbt()
    analysis = AnalysisData.analyze(game)

    nfg = f"""<nfgfile>
{game.write()}</nfgfile>

<profile>
{','.join([f'{r[0]}/{r[1]}' for r in analysis.p1_probs])
 },{','.join([f'{r[0]}/{r[1]}' for r in analysis.p2_probs])}
</profile>"""

    with tempfile.NamedTemporaryFile(delete=False) as fp:
        fp.write(nfg.encode())
        temp_file_name = fp.name
    return FileResponse(temp_file_name, filename="game.gbt")


@app.post("/upload")
async def upload_file(file: UploadFile):
    """Receive a file and return the corresponding MixupData object"""

    contents = await file.read()
    game = gbt.Game.parse_game(contents.decode())
    mixupData = MixupData.from_gbt(game)
    return mixupData.model_dump()

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
