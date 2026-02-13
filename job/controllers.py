from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from job.models import JobModel
from job.schemas import JobResponseSchema, JobCreateSchema, JobUpdateSchema
from core.auth import get_current_user
from core.database import get_db
from user.models import UserModel

router = APIRouter(tags=["job"], prefix="/jobs")


@router.get("/", response_model=List[JobResponseSchema])
async def retrive_job_list(job_name: str= None,
                           db: Session = Depends(get_db),
                           current_user: UserModel = Depends(get_current_user)
                           ):
    if job_name:
        last_week = datetime.now() - timedelta(days=7)
        jobs = db.query(JobModel).filter(
            JobModel.job_name == job_name,
            JobModel.run_time >= last_week
        ).all()
    else:
        jobs = db.query(JobModel).all()
    return jobs


@router.get("/{job_id}/", response_model=JobResponseSchema)
async def retrieve_job_detail(job_id: int,
                              db: Session = Depends(get_db),
                              current_user: UserModel = Depends(get_current_user)
                              ):
    job = db.query(JobModel).filter_by(id=job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    return job


@router.post("/")
async def create_job(request_job: JobCreateSchema,
                     db: Session = Depends(get_db),
                     current_user: UserModel = Depends(get_current_user)
                     ):
    job_data = request_job.model_dump()
    job = JobModel(**job_data)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.put("/{job_id}/")
async def create_job(job_id: int, request_job: JobUpdateSchema,
                     db: Session = Depends(get_db),
                     current_user: UserModel = Depends(get_current_user)
                     ):
    job = db.query(JobModel).filter_by(id=job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    job_data = request_job.model_dump()

    for key, item in job_data.items():
        setattr(job, key, item)

    db.commit()
    db.refresh(job)
    return job


@router.delete("/{job_id}/", status_code=204)
async def delete_job(job_id: int,
                     db: Session = Depends(get_db),
                     current_user: UserModel = Depends(get_current_user)
                     ) -> None:
    job = db.query(JobModel).filter_by(id=job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    db.delete(job)
    db.commit()
