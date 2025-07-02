from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from services.supabase_client import get_user_tokens
from utils.token_handler import check_and_refresh_token
from services.ga4_client import get_session_count
import asyncio
import json

router = APIRouter()

@router.post("/get-sessions-sse")
async def get_sessions_sse(request: Request):
    body = await request.json()
    
    user_id = body.get("userId")
    ga_data = body.get("googleAnalyticsData", {})
    property_id = ga_data.get("selectedProperty", {}).get("id")

    async def stream():
        # Step 1: Validate input
        if not user_id or not property_id:
            yield f"data: {json.dumps({'error': 'Missing userId or GA4 property ID'})}\n\n"
            return

        # Step 2: Get tokens from Supabase
        tokens = get_user_tokens(user_id)
        if not tokens:
            yield f"data: {json.dumps({'error': 'No credentials found for this user'})}\n\n"
            return

        # Step 3: Refresh tokens if expired
        try:
            tokens = await check_and_refresh_token(user_id, tokens)
        except Exception as e:
            yield f"data: {json.dumps({'error': f'Token refresh failed: {str(e)}'})}\n\n"
            return

        # Step 4: Query GA4 API
        try:
            yield f"data: {json.dumps({'message': 'Fetching session data from GA4...'})}\n\n"
            await asyncio.sleep(0.6)  # small delay for streaming effect

            result = await get_session_count(tokens["access_token"], property_id)

            if result["value"] == "0":
                yield f"data: {json.dumps({'message': 'Success, but no sessions found.', 'data': result})}\n\n"
            else:
                yield f"data: {json.dumps({'message': '✅ Session count retrieved', 'data': result})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': f'Google Analytics API error: {str(e)}'})}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")
