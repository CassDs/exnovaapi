"""Module for exnova buyV2 websocket chanel."""
from datetime import datetime, timedelta
from exnovaapi.ws.chanels.base import Base
from exnovaapi.expiration import get_expiration_time


class Buyv2(Base):
    """Class for Exnova buy websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "sendMessage"

    def __call__(self, price, active, direction, duration):
        """Method to send message to buyv2 websocket chanel.
        :param price: The buying price.
        :param active: The buying active.
        :param direction: The buying direction.
        """

        exp, idx = get_expiration_time(
            int(self.api.timesync.server_timestamp), duration)

        if idx < 5:
            option = 3  # turbo
        else:
            option = 1  # non-turbo / binary

        data = {
            "price": price,
            "act": active,
            "exp": int(exp),
            "type": option,
            "direction": direction.lower(),
            "user_balance_id": int(self.api.context.balance_id),
            "time": self.api.timesync.server_timestamp
        }

        self.send_websocket_request(self.name, data)
