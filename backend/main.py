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