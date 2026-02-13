from datetime import date

from pydantic import BaseModel, Field


class JobBaseSchema(BaseModel):
    job_name: str = Field(..., max_length=100)
    job_type: str = Field(..., max_length=100)
    Job_date: date = Field(...)


class JobCreateSchema(JobBaseSchema):
    pass


class JobUpdateSchema(JobBaseSchema):
    job_name: str | None = None
    job_type: str | None = None
    Job_date: date | None = None


class JobResponseSchema(JobBaseSchema):
    id: int

    model_config = {
        "from_attribute": True
    }