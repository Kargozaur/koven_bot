import re
import urllib.parse

from httpx import AsyncClient

from src.core.settings.rio_settings import RioSettings
from src.params.char_params import CharParamns


class RaiderIOService:
    URL_PATTERN: re.Pattern[str] = re.compile(
        r"raider\.io/characters/(?P<region>[a-z]{2,3})/(?P<realm>[a-z0-9-]+)/(?P<name>[^/?#\s]+)",
        re.IGNORECASE,
    )

    def __init__(self, client: AsyncClient, rio_settings: RioSettings) -> None:
        self.client = client
        self.rio_settings = rio_settings

    def _extract_params_from_url(self, url: str) -> CharParamns | None:
        decoded_url = urllib.parse.unquote(url).strip()
        print(f"DECODED URL: {decoded_url}")
        match = self.URL_PATTERN.search(decoded_url)
        if not match:
            print("DEBUG: regex failed")
            return None

        try:
            params = CharParamns(**match.groupdict())
            print(f"DEBUG: created params {params}")
            return params
        except Exception as e:
            print(f"DEBUG: Pydantic validation failed {e}")
            return None

    async def fetch_character(self, params: CharParamns) -> dict | None:
        api_url = "https://raider.io/api/v1/characters/profile"
        query_params = {
            "region": params.region,
            "realm": params.realm,
            "name": params.name,
            "fields": "mythic_plus_scores_by_season:current",
        }
        print(f"DEBUG: Requesting API {api_url} params={query_params}")
        token = self.rio_settings.key.get_secret_value()
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        try:
            response = await self.client.get(
                url=api_url, params=query_params, headers=headers
            )
            print(f"DEBUG: API status: {response.status_code}")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"DEBUG: Failed to fetch data from API: {e}")

        return None
