import aiohttp
from typing import Union, Dict, Any
from config import FGIS_API_ENDPOINT


async def search(mi: str, mit: Union[str, None] = None) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        if mit is None:
            params = {"org_title": "ООО Квазар", "mi_number": mi}
        else:
            params = {"mi_number": mi, "mit_number": mit}

        async with session.get(FGIS_API_ENDPOINT, params=params) as response:
            result = await response.json()
        return result

    