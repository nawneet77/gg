from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import json

router = APIRouter()

@router.get("/sse")
async def mcp_sse():
    async def stream():
        # Tool manifest for n8n AI Agent
        tool_manifest = {
            "tools": [
                {
                    "name": "get_sessions",
                    "description": "Fetch GA4 session count for the last 30 days",
                    "endpoint": "/ga4/get-sessions-sse",
                    "method": "POST",
                    "parameters": [
                        {"name": "userId", "type": "string", "required": True},
                        {"name": "googleAnalyticsData", "type": "object", "required": True}
                    ]
                }
            ]
        }

        yield f"data: {json.dumps(tool_manifest)}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")
