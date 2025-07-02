from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import json
import asyncio

router = APIRouter()

@router.get("/sse")
async def mcp_sse():
    async def stream():
        tool_manifest = {
            "tools": [
                {
                    "name": "get_sessions",
                    "description": "Fetch GA4 session count for the last 30 days",
                    "endpoint": "/ga4/get-sessions-sse",
                    "method": "POST",
                    "parameters": [
                        {
                            "name": "userId",
                            "type": "string",
                            "description": "The Supabase user ID",
                            "required": True
                        },
                        {
                            "name": "googleAnalyticsData",
                            "type": "object",
                            "description": "GA4 tokens and property info from client",
                            "required": True
                        }
                    ]
                }
            ]
        }

        # Initial event stream (manifest)
        yield f"data: {json.dumps(tool_manifest)}\n\n"

        # Optional: Keep-alive to prevent connection drop
        while True:
            await asyncio.sleep(25)
            yield ":\n\n"  # SSE comment = keep alive

    return StreamingResponse(stream(), media_type="text/event-stream")
