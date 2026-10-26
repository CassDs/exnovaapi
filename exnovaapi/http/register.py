"""Module for exnovaapi register resource."""

import requests
from exnovaapi.http.resource import Resource


class Register(Resource):
    """Class for exnovaapi register resource."""
    # pylint: disable=too-few-public-methods

    url = "https://auth.trade.exnova.com/api/v3/register"

    def _post(self, data=None, headers=None):
        hdrs = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
        if headers:
            hdrs.update(headers)
        return requests.post(self.url, json=data, headers=hdrs, timeout=10)

    def __call__(self, username, password, country_id=30, first_name="", last_name=""):
        data = {
            "identifier": username,
            "password": password,
            "accepted": ["terms", "privacy policy"],
            "country_id": int(country_id),
        }
        if first_name:
            data["first_name"] = first_name
        if last_name:
            data["last_name"] = last_name
        return self._post(data=data)
