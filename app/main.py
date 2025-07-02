from fastapi import FastAPI
from routes import tools, ga4, sessions_sse, mcp_sse

app = FastAPI(title="MCP GA4 Tool Server")

app.include_router(tools.router, prefix="/mcp")
app.include_router(mcp_sse.router, prefix="/mcp")  # ⬅️ GET /mcp/sse for manifest
app.include_router(ga4.router, prefix="/ga4")
app.include_router(sessions_sse.router, prefix="/ga4")  # ⬅️ POST /ga4/get-sessions-sse
