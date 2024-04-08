import asyncio
import json
from dotenv import load_dotenv
import os
from uptime_kuma_api import UptimeKumaApi as kumaApi


async def get_all_monitors():
    api = kumaApi(os.getenv('KUMA_API_LINK'))
    api.login(os.getenv('KUMA_API_USERNAME'), os.getenv('KUMA_API_PASSWORD'))
    monitor_list = api.get_monitors()

    results = []
    for monitor in monitor_list:
        beats = api.get_monitor_beats(monitor['id'], 24)
        results.append({
            "name": monitor['name'],
            "status": beats[-1]['status'],
            "ping": beats[-1]['ping']
        })

    api.disconnect()
    return results
