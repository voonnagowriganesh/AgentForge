from pydantic import BaseModel


class PlanStep(BaseModel):

    step: int
    task: str | None = None

    input: str

    tool: str | None = None


class Plan(BaseModel):
    plan: list[PlanStep]
