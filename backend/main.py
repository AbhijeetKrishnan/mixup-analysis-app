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
    p1_probs: Optional[List[Tuple[int, int]]] = None
    p2_probs: Optional[List[Tuple[int, int]]] = None
    payoff: Optional[Tuple[int, int]] = None

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

    def analyze(self) -> None:
        """Analyze the game and store the mixed strategy probabilities"""

        game = self.to_gbt()
        solver = gbt.nash.lp_solve
        eqa = solver(game)
        profile = eqa[0]
        self.p1_probs = [profile[game.players[0]][strategy].as_integer_ratio(
        ) for strategy in game.players[0].strategies]
        self.p2_probs = [profile[game.players[1]][strategy].as_integer_ratio(
        ) for strategy in game.players[1].strategies]
        self.payoff = profile.payoff(game.players[0]).as_integer_ratio()

    @classmethod
    def from_gbt(cls, game: gbt.Game) -> "MixupData":
        """Converts a pygambit game to form data with analysis results"""

        rows = len(game.players[0].strategies)
        cols = len(game.players[1].strategies)
        matrix = [[0 for _ in range(cols)] for _ in range(rows)]

        for contingency in game.contingencies:
            try:
                value = game[contingency][game.players[0]]
            except RuntimeError:  # 0 outcome results in dereferenced null pointer error on pygambit
                value = 0
            matrix[contingency[0]][contingency[1]] = value

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
        mixupData.analyze()

        return mixupData


@router.post("/analyze")
def analyze_game(mixupData: MixupData):
    mixupData.analyze()
    return mixupData.model_dump()


@app.post("/download")
def download_game(mixupData: MixupData):
    game = mixupData.to_gbt()
    mixupData.analyze()
    nfg = f"""<nfgfile>
{game.write()}</nfgfile>

<profile>
{','.join([f'{r[0]}/{r[1]}' for r in mixupData.p1_probs])
 },{','.join([f'{r[0]}/{r[1]}' for r in mixupData.p2_probs])}
</profile>"""
    with tempfile.NamedTemporaryFile(delete=False) as fp:
        fp.write(nfg.encode())
        temp_file_name = fp.name
    return FileResponse(temp_file_name, filename="game.gbt")


@app.post("/upload")
async def upload_file(file: UploadFile):
    contents = await file.read()
    game = gbt.Game.parse_game(contents.decode())
    mixupData = MixupData.from_gbt(game)
    return mixupData.model_dump()

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
