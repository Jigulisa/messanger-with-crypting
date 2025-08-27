from pathlib import Path
from typing import Self

from litestar import Controller, get


class AIController(Controller):
    models_dir = Path(__file__).resolve().parent.parent.parent / "ai_models/"

    @get("/spam-tracker")
    async def get_spam_tracker_model(self: Self) -> bytes:
        with (self.models_dir / "spam_tracker.tar.xz").open("rb") as file:
            return file.read()

    @get("/summarization")
    async def get_summarization_model(self: Self) -> bytes:
        with (self.models_dir / "summarization.tar.xz").open("rb") as file:
            return file.read()

    @get("/auto-answer")
    async def get_auto_answer_model(self: Self) -> bytes:
        with (self.models_dir / "auto_answer.tar.xz").open("rb") as file:
            return file.read()
