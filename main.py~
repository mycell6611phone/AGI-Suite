from fastapi import FastAPI
from pydantic import BaseModel
from memory_fabric.memory_fabric import MemoryFabric
from plugin_toolbelt.plugin_manager import PluginManager
from metacog_core.meta_planner import MetaPlanner

app = FastAPI(
    title="AGI Suite",
    description="Modular, server-first AGI agent platform",
    version="0.1.0"
)

memory = MemoryFabric()
plugins = PluginManager()
planner = MetaPlanner()

class AskRequest(BaseModel):
    input: str

@app.post("/agent/ask")
async def agent_ask(request: AskRequest):
    user_input = request.input
    memory_context = memory.retrieve(user_input)
    plan = planner.plan(user_input, memory_context)
    response = plugins.run(plan)
    return {
        "result": response,
        "memory_context": memory_context
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

