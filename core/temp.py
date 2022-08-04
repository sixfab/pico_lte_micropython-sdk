"""
Basic module for using purpose of provining temporary memory
for sharing data by different modules.
"""

from core.utils.debug import Debug, DebugChannel

class StateCache:
    """Data class for storing state data"""

    states = {}

    def add_cache(self, function_name):
        """Gets cache for #function_name or adds new cache with #function_name key"""
        if not self.states.get(function_name):
            self.states[function_name] = None

    def get_state(self, function_name):
        """Returns state of function_name"""
        return self.states.get(function_name)

    def set_state(self, function_name, state):
        """Sets state of function_name"""
        self.states[function_name] = state

config = {}
cache = StateCache()
debug = Debug()
config["cache"] = cache
