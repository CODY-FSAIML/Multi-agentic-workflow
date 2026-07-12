import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base
import datetime

class WorkflowJob(Base):
    __tablename__ = "workflow_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(String, default="queued")  # queued, processing, completed, failed
    user_prompt = Column(String, nullable=False)
    final_result = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationship to track individual agent steps
    logs = relationship("AgentLog", back_populates="job", cascade="all, delete-orphan")

class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("workflow_jobs.id"))
    agent_name = Column(String, nullable=False)  # e.g., Router, Researcher, Writer
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    status = Column(String, default="processing") # processing, completed, failed
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    job = relationship("WorkflowJob", back_populates="logs")