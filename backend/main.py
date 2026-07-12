
import database
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from uuid import UUID
import models, schemas
from database import get_db
from celery_worker import run_multi_agent_workflow

app = FastAPI(title="Distributed Multi-Agent System")
models.Base.metadata.create_all(bind=database.engine)

@app.post("/api/v1/agents/workflow", status_code=202)
def start_workflow(payload: schemas.WorkflowCreate, db: Session = Depends(get_db)):
    # 1. Create a record in the database
    db_job = models.WorkflowJob(user_prompt=payload.prompt, status="queued")
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    # 2. Push the task into the Redis queue for Celery to pick up
    run_multi_agent_workflow.delay(str(db_job.id), payload.prompt)

    # 3. Return tracking information immediately (< 50ms)
    return {
        "workflow_id": db_job.id,
        "status": db_job.status,
        "check_status_url": f"/api/v1/agents/workflow/{db_job.id}"
    }

@app.get("/api/v1/agents/workflow/{workflow_id}")
def get_workflow_status(workflow_id: UUID, db: Session = Depends(get_db)):
    job = db.query(models.WorkflowJob).filter(models.WorkflowJob.id == workflow_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Workflow job not found")
    
    # Return current status, logs of steps completed so far, and final result if done
    return {
        "workflow_id": job.id,
        "status": job.status,
        "logs": [{"agent": log.agent_name, "status": log.status} for log in job.logs],
        "final_result": job.final_result
    }
=======
from fastapi import FastAPI
from pydantic import BaseModel
from worker import test_agent_task

app = FastAPI(title="Multi-Agent API")

class TaskRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"message": "Backend is live and running!"}

@app.post("/run-agent")
def run_agent(request: TaskRequest):
    # Send the heavy lifting to Celery in the background
    task = test_agent_task.delay(request.prompt)
    return {"task_id": task.id, "message": "Agent task submitted to queue"}

