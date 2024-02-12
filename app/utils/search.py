import aiohttp, aiofiles
from bs4 import BeautifulSoup
import asyncio
import json
from config import FGIS_API_ENDPOINT


async def get_vri_data(str):
    soup = BeautifulSoup(str)
    return soup.get_text()


async def search(mi: str, mit: str | None = None) -> (dict, str):
    async with aiohttp.ClientSession() as session:
        if mit is not None:
            params = {"mi_number": mi, "mit_number": mit}
        else:
            params = {"org_title": 'ООО "КВАЗАР"', "mi_number": mi}
        async with session.get(FGIS_API_ENDPOINT, params=params) as raw_vri:
            result = await raw_vri.json()
            if not result["result"]["items"]:
                return (None, None)
            vri_id = result["result"]["items"][0]["vri_id"]

        await asyncio.sleep(2)

        async with session.get(FGIS_API_ENDPOINT + "/" + vri_id) as raw_vri_data:
            text_vri_data = text_vri_data = await get_vri_data(
                await raw_vri_data.text("utf-8")
            )
            vri_data = json.loads(text_vri_data)

        async with aiofiles.open("FFS.txt", "a+") as file:
            for key in vri_data.keys():
                await file.write(f"{key} : {vri_data[key]}")

    return (vri_data["result"], vri_id)
