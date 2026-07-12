from pydantic import BaseModel

class WorkflowCreate(BaseModel):
    prompt: str