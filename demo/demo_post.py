
import requests
import asyncio

async def get_posthog_events(api_key, project_id, start_date, end_date):
    # Set the request headers.
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    # Set the request parameters.
    params = {
        "project_id": project_id,
        "start_date": start_date,
        "end_date": end_date,
    }

    # Make the request.
    async with requests.get("https://app.posthog.com/api/v1/events", headers=headers, params=params) as response:
        # Check if the request was successful.
        response.raise_for_status()

        # Return the list of events.
        return await response.json()

