#python
"""
Context class for managing per-instance state.
This replaces the global_value module to support multiple simultaneous connections.
"""

class ExnovaContext:
    """
    Per-instance context that holds all the state that was previously global.
    Each Exnova/ExnovaAPI instance has its own context.
    """

    def __init__(self):
        # Connection state
        self.check_websocket_if_connect = None
        self.check_websocket_if_error = False
        self.websocket_error_reason = None

        # Session ID
        self.SSID = None

        # Balance ID
        self.balance_id = None

        # SSL mutex flags (for thread safety within this instance)
        self.ssl_Mutual_exclusion = False
        self.ssl_Mutual_exclusion_write = False
