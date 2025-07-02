from fastapi import APIRouter

router = APIRouter()

@router.get("/tools")
async def list_tools():
    return [
        {
            "name": "ga4_get_sessions",
            "description": "Get the number of sessions in the last 30 days from Google Analytics 4.",
            "parameters": {
                "type": "object",
                "properties": {
                    "userId": {"type": "string", "description": "User ID used to fetch GA4 credentials"},
                    "property_id": {"type": "string", "description": "Google Analytics 4 Property ID"}
                },
                "required": ["userId", "property_id"]
            }
        }
    ]
