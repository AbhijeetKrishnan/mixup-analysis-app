from typing import List, Tuple, Optional
import tempfile

from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import pygambit as gbt
import numpy as np
import uvicorn

app = FastAPI()


class MixupData(BaseModel):
    title: str = Field(default="Untitled strategic game")
    comment: str = Field(default="")
    player_1: str = Field(default="1")
    player_2: str = Field(default="2")
    p1_strategies: List[str] = None
    p2_strategies: List[str] = None
    rows: int
    cols: int
    data: List[List[int]]
    p1_probs: Optional[List[Optional[Tuple[int, int]]]] = None
    p2_probs: Optional[List[Optional[Tuple[int, int]]]] = None
    payoff: Optional[Tuple[int, int]] = None

    def to_gbt(self) -> gbt.Game:
        """Converts the form data to a pygambit game"""

        payoff_matrix = np.array(self.data)
        game = gbt.Game.from_arrays(payoff_matrix, -payoff_matrix, title=self.title)
        
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
        self.p1_probs = [eqa[0].strategy_value(strategy).as_integer_ratio() for strategy in game.players[0].strategies]
        self.p2_probs = [eqa[0].strategy_value(strategy).as_integer_ratio() for strategy in game.players[1].strategies]
        self.payoff = eqa[0].payoff(game.players[0]).as_integer_ratio()
    
    @classmethod
    def from_gbt(cls, game: gbt.Game) -> "MixupData":
        """Converts a pygambit game to form data with analysis results"""

        rows = len(game.players[0].strategies)
        cols = len(game.players[1].strategies)
        data = [[0 for _ in range(cols)] for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                value = game.outcomes[i * cols + j][game.players[0]].numerator
                data[i][j] = value

        mixupData = MixupData(
            title=game.title,
            comment=game.comment,
            player_1=game.players[0].label,
            player_2=game.players[1].label,
            p1_strategies=[s.label for s in game.players[0].strategies],
            p2_strategies=[s.label for s in game.players[1].strategies],
            rows=rows,
            cols=cols,
            data=data
        )
        mixupData.analyze()

        return mixupData


@app.post("/analyze")
def analyze_game(mixupData: MixupData):
    mixupData.analyze()
    return mixupData.model_dump()

@app.post("/download")
def download_game(mixupData: MixupData):
    game = mixupData.to_gbt()
    nfg = game.write()
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


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)