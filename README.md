# Multi-Agentic Workflow System

A high-performance, distributed multi-agent system designed for asynchronous AI task execution.

## 🚀 Architecture
This system utilizes a robust asynchronous architecture to handle high-volume requests:
- **FastAPI**: Low-latency API Gateway.
- **Celery + Redis**: Distributed task queue for non-blocking agent execution.
- **PostgreSQL**: Persistent storage for workflow status and agent logs.
- **Docker**: Containerized environment for consistent deployment.

## 🛠 Features
- **State Machine Loop**: Orchestrates multi-agent logic without heavy frameworks.
- **Fault Tolerance**: Implements exponential backoff (Tenacity) to handle LLM rate-limiting.
- **Polling Pattern**: Provides asynchronous status tracking for long-running AI tasks.

## 🏗 Setup Instructions
1. Clone the repository:
   `git clone https://github.com/YOUR-USERNAME/multi-agentic-workflow.git`
2. Configure your environment:
   Create a `.env` file with `DATABASE_URL`, `REDIS_URL`, and `LLM_API_KEY`.
3. Launch the environment:
   `docker-compose up --build`
4. Access the API documentation at `http://localhost:8000/docs`.