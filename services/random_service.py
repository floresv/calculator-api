import requests  # type: ignore[import-untyped]
import string


class RandomService:
    def __init__(self) -> None:
        self.base_api_url = "https://www.random.org/"

    def base_params(self) -> dict:
        return {
            "num": 1,
            "len": 10,
            "digits": "on",
            "upperalpha": "on",
            "loweralpha": "on",
            "unique": "on",
            "format": "plain",
            "rnd": "new",
        }

    def generate_random_string(self, params={}) -> str:
        """
        Get random string
        """
        merged_params = {**self.base_params(), **params}
        params_url = "&".join(
            [f"{key}={value}" for key, value in merged_params.items()]
        )
        service_url = self.base_api_url + "/strings/?"

        response = requests.get(service_url + params_url)
        if response.status_code == 200:
            return response.text.replace("\n", "")
        else:
            raise Exception(f"Error fetching random string: {response.status_code}")
