from datetime import datetime

from pydantic import BaseModel, Field


class JobBaseSchema(BaseModel):
    job_name: str = Field(..., max_length=100)
    run_type: str = Field(..., max_length=100)
    run_time: datetime = Field(..., example="2026-02-13 15:30:40")


class JobCreateSchema(JobBaseSchema):
    pass


class JobUpdateSchema(JobBaseSchema):
    job_name: str | None = None
    run_type: str | None = None
    run_time: datetime | None = None


class JobResponseSchema(JobBaseSchema):
    id: int

    model_config = {
        "from_attribute": True
    }