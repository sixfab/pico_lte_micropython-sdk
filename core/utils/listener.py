"""
Module for listening modem responses and handling them.
"""

from core.temp import debug


class ModemResponse:
    def __init__(self, response, callback=None):
        self.response = response
        self.callback = callback


class Listener:
    LINE_END = "\n"
    MAX_UNDEFINED_LEN = 1000 # max buffer size for undefined responses
    defined_responses = []

    def __init__(self, atcom):
        self.atcom = atcom

    def add_defined_response(self, response, callback=None):
        """
        Function for adding defined response to listener
        """
        self.defined_responses.append(ModemResponse(response, callback))

    def run_once(self):
        """
        Function for processing received message
        """
        self.atcom.listen_and_save_messages()

        if self.atcom.buffer.any_data():
            message = self.atcom.buffer.get_message()

            debug.debug("buffer before process:", [self.atcom.buffer.get_message()])

            for state in self.defined_responses:
                if state.response in message:
                    start_of_message = message.find(state.response)

                    # clear meaningless data from buffer
                    self.atcom.buffer.clear_before_id(start_of_message)
                    end_off_message = message[start_of_message:].find(self.LINE_END) + start_of_message
                    desired_message = message[start_of_message:end_off_message]

                    # clear processed message from buffer
                    self.atcom.buffer.clear_before_id(end_off_message)

                    debug.debug("Processed Message:", desired_message)
                    debug.debug("Buffer after process:", [self.atcom.buffer.get_message()])

                    if state.callback:
                        debug.debug("Callback running...")
                        state.callback(desired_message)
            # if buffer has to many meaningless messages, clear it
            if self.atcom.buffer.any_data() > self.MAX_UNDEFINED_LEN:
                self.atcom.buffer.clear()
