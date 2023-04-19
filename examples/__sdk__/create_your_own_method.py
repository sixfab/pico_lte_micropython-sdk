"""
This example is aim to find out how to use manager utility of picocell SDK.
Manager is a utility to manage the complicated processes have multiple steps,
specific execution order, need of response binded decision, etc.

In this example we will use manager to perform HTTP POST request to a server.
We will explain how to create a method by using manager step by step.

Example Configuration
---------------------
Create a config.json file in the root directory of the picocell device.
config.json file must include the following parameters for this example:

config.json
{
    "https":{
        "server":"[HTTP_SERVER]",
        "username":"[YOUR_HTTP_USERNAME]",
        "password":"[YOUR_HTTP_PASSWORD]"
    },
}
"""
import time

from pico_lte.utils.status import Status
from pico_lte.utils.manager import StateManager, Step
from pico_lte.modem import Modem


# First of all we need to create the function
def our_http_post_method(message):
    """Function for performing HTTP POST request to a server."""

    # create instance of Modem class
    modem = Modem()

    # Creating step 1. In this case this step
    # will check the network registeration status
    # and if it is not registered then it will

    step_check_network = Step(
        name="check_network", # name of the step
        function=modem.network.register_network, # function to be executed
        success="prepare_pdp", # if succied then go to next step
        fail="failure", # if failed then go to next step
        retry=3 # number of retries if failed without going on the failure step
    )

    # "success", "failure" and "organizer" steps are built-in.
    # They are defined in the manager class.

    # Creating step 2.
    # In this step we will check the PDP status

    step_prepare_pdp = Step(
        name="prepare_pdp",
        function=modem.network.get_pdp_ready,
        success="set_server_url",
        fail="failure",
    )

    # Creating step 3.
    # In this step we will set the server URL
    # modem.http.set_server_url function gets server URL from
    # the config.json file automatically. You must just create a
    # config.json file and put it in the picocell root path.

    step_set_server_url = Step(
        name="set_server_url",
        function=modem.http.set_server_url,
        success="post_request",
        fail="failure",
    )

    # Creating step 4.
    # In this step we will send the POST request
    # We will pass the function_params as a dictionary
    # "data" is the name of argument that will be passed to the function
    # message is the value of argument that will be passed to the function
    # it acts like --> function(data=message)

    step_post_request = Step(
        name="post_request",
        function=modem.http.post,
        success="read_response",
        fail="failure",
        function_params={"data": message},
        interval=3, # interval in seconds between each steps and retries
    )

    # Creating step 5.
    # In this step we will read the response of server.
    # We will use the "read_response" step to check the response status.
    # If the response status is 200, the post request is successful.
    # if the response status is 400 or 404, then function will return failure

    step_read_response = Step(
        name="read_response",
        function=modem.http.read_response,
        success="success",
        fail="failure",
        function_params={
            "desired_response": ["200"],
            "fault_response": ["400","404"]
            },
    )

    # We created all required steps.
    # Now we will create the manager object and add all steps to it.

    manager = StateManager()
    manager.add_step(step_check_network)
    manager.add_step(step_prepare_pdp)
    manager.add_step(step_set_server_url)
    manager.add_step(step_post_request)
    manager.add_step(step_read_response)

    # Now we will execute the manager.
    # Manager will execute all steps in the order.
    # If the step is successful, it will go to it's success step.
    # If the step is failed, it will go to it's failure step.

    while True: # Create an infinite loop to keep the manager running.
        result = manager.run() # Run the manager.

        if result["status"] == Status.SUCCESS: # If the manager is successful, then break the loop.
            return result
        elif result["status"] == Status.ERROR: # If the manager is failed, then break the loop.
            return result
        time.sleep(result["interval"]) # If manager is still running, then wait for the interval.


# Now we can use the function
# We will pass "Hello World" as a message to the function.

our_http_post_method("Hello World")
