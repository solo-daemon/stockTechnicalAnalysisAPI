from app.database import (
   update_user_rate_data_in_db,
   get_user_info_from_db 
)
import time 

last_sync = {}  # {user_id: timestamp}

async def sync_rate_data_to_db(client, user_id: str, current_window: int):
    key = f"rate:{user_id}:{current_window}"
    now = time.time()

    # Only sync once per minute per user
    if user_id in last_sync and now - last_sync[user_id] < 60:
        return

    current = await client.get(key)
    if current:
        count = int(current)
        await update_user_rate_data_in_db(user_id, current_window, count)
        last_sync[user_id] = now