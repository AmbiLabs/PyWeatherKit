# weatherkit/client.py
# A third-party library for Apple's WeatherKit API.
# Copyright 2022 David Kopec
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import requests
from weatherkit.token import generate_token, Token
from time import time
from dataclasses import dataclass
import typing


class TokenExpiredError(Exception):
    pass

@dataclass
class WKClient:
    # Generates a WKClient that can connect to WeatherKit.
    # *key_path* should be the path to a private key file.
    # *expiry* is the number of seconds the client should be valid for.
    # *team_id* is the 10 digit Apple Developer team id
    # *key_id* is the 10 digit id associated with the private key.
    # *service_id* is the custom id you specified when you created the service.
    team_id: str
    service_id: str
    key_id: str
    key_path: str
    expiry: int = 3600
    token: Token = None

    # Returns the current weather for *latitude* and *longitude*.
    # *latitude* and *longitude* are floats.
    # *language* is a string representing the language to use as a 2 letter code.
    # *timezone* is a string representing the timezone to use.
    # *dataSets* is a list of strings representing the data sets to return which can include:
    # currentWeather, forecastDaily, forecastHourly, forecastNextHour, or weatherAlerts
    def get_weather(self, latitude: float, longitude: float, language: str = "en", timezone: str = "America/Swift_Current",
                    dataSets: typing.List[str] = ["currentWeather", "forecastHourly"]) -> dict:
        if not self.token or self.token.expiry_time < time():
            self.token = generate_token(self.team_id, self.service_id, self.key_id, self.key_path, self.expiry)
        url = f"https://weatherkit.apple.com/api/v1/weather/{language}/{latitude}/{longitude}"
        headers = {
            "Authorization": f"Bearer {self.token.token}"
        }
        params = {
            "timezone": timezone,
            "dataSets": ",".join(dataSets)
        }
        response = requests.get(url, headers=headers, params=params)

        return response.json()


