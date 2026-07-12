import os
from celery import Celery

# Grab the Redis URL from the environment variables we set in docker-compose
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Initialize Celery
celery = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# This is a dummy task where your agent logic will eventually live
@celery.task(name="test_agent_task")
def test_agent_task(prompt: str):
    print(f"Agent received prompt: {prompt}")
    return {"status": "completed", "result": f"Processed: {prompt}"}