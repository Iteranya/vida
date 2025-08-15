# main.py

from fastapi import FastAPI

# Import the logic from our other file
from agent_manager import AgentManager, AgentDataClass

app = FastAPI(
    title="Agent Management API",
    description="An API to create, read, update, and delete AI agents.",
    version="1.0.0",
)

@app.get("/", include_in_schema=False)
def root():
    return {"message": "Still Under Construction."}
