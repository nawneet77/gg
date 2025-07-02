from fastapi import FastAPI
from routes import tools, ga4

app = FastAPI(title="MCP GA4 Tool Server")

# Register the GA4 router
app.include_router(tools.router, prefix="/mcp")
app.include_router(ga4.router, prefix="/ga4")

from routes import sessions_sse
app.include_router(sessions_sse.router, prefix="/ga4")
