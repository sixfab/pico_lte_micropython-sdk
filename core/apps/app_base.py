"""
Base class module for all apps to inherit from.

How to Implement a New App:
1. Create a new file in the `core/apps` directory.
2. Inherit the `AppBase` class.
3. Implement the abstract methods.
4. Initilize the app on the `PicoLTE` as an attribute in `core/pico_lte.py` file.

Functions to Implement for HTTP:
* __post_message_on_cellular
* __post_message_on_wifi
* __post_message_on_both

Functions to Implement for MQTT:
* __publish_message_on_cellular
* __publish_message_on_wifi
* __publish_message_on_both
"""

from time import sleep
from core.utils.enums import Connection, Status
from core.utils.manager import StateManager, Step


class AppBase:
    """Base class for all apps to inherit from."""

    def __init__(self, cellular, wifi):
        self.cellular = cellular
        self.wifi = wifi

    def publish_message(self, *args, via=Connection.BOTH, **kwargs):
        """A function to MQTT publish a message to the server."""
        if via == Connection.CELLULAR:
            return self.__publish_message_on_cellular(*args, **kwargs)
        elif via == Connection.WIFI:
            return self.__publish_message_on_wifi(*args, **kwargs)
        else:
            return self.__publish_message_on_both(*args, **kwargs)

    def post_message(self, *args, via=Connection.BOTH, **kwargs):
        """A function to HTTP post a message to the server."""
        if via == Connection.CELLULAR:
            return self.__post_message_on_cellular(*args, **kwargs)
        elif via == Connection.WIFI:
            return self.__post_message_on_wifi(*args, **kwargs)
        else:
            return self.__post_message_on_both(*args, **kwargs)

    # Will be implemented in the child classes.
    # @abstractmethod
    def __publish_message_on_cellular(
        self, *args, message, host, port, topic, client_id, username, **kwargs
    ):
        """A function to publish a message to the MQTT broker using cellular connection."""
        raise NotImplementedError

    # Will be implemented in the child classes.
    # @abstractmethod
    def __publish_message_on_wifi(
        self, *args, message, host, port, topic, client_id, username, **kwargs
    ):
        """A function to publish a message to the MQTT broker using WiFi connection."""
        raise NotImplementedError

    def __publish_message_on_both(self, app_name, params):
        """A function to publish a message to the MQTT broker
        using both WiFi and cellular connections."""
        step_try_wifi = Step(
            name=f"{app_name}_send_message_on_wifi",
            function=self.__publish_message_on_wifi,
            function_params=params,
            success="success",
            fail="send_message_on_cellular",
        )

        step_try_cellular = Step(
            name=f"{app_name}_send_message_on_cellular",
            function=self.__publish_message_on_cellular,
            function_params=params,
            success="success",
            fail="failure",
        )

        state_manager = StateManager(
            function_name=f"{app_name}_send_message_on_both",
            first_step=step_try_wifi
        )

        state_manager.add_step(step_try_wifi)
        state_manager.add_step(step_try_cellular)

        while True:
            result = state_manager.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            sleep(result["interval"])

    # Will be implemented in the child classes.
    # @abstractmethod
    def __post_message_on_cellular(self, *args, message, host, **kwargs):
        """A function to post a message to the server using cellular connection."""
        raise NotImplementedError

    # Will be implemented in the child classes.
    # @abstractmethod
    def __post_message_on_wifi(self, *args, message, host, **kwargs):
        """A function to post a message to the server using WiFi connection."""
        raise NotImplementedError

    # Will be implemented in the child classes.
    # @abstractmethod
    def __post_message_on_both(self, *args, message, host, **kwargs):
        """A function to post a message to the server using both WiFi and cellular connections."""
        raise NotImplementedError
