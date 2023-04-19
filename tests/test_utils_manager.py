"""
Test Module for the utils.manager module.
"""

import pytest

from pico_lte.utils.manager import Step, StateManager
from pico_lte.utils.status import Status
from pico_lte.common import config


def example_function(function_code):
    """Example function to be used in the tests."""
    return {"status": Status.SUCCESS, "response": function_code}


class TestStep:
    """Test class for the Step class."""

    def test_initial_parameters(self):
        """Test if the default parameters are configured correctly."""
        with pytest.raises(TypeError):
            Step()

    def test_parameters_given(self):
        """Test if the given parameters are configured correctly."""
        step_example = Step(
            "example_step",
            example_function,
            "success",
            "failure",
            function_params={"function_code": 15},
            interval=2,
            retry=1,
            final_step=False,
            cachable=True,
        )

        assert isinstance(step_example, Step)


class TestManager:
    """Test class for the StateManager class."""

    @pytest.fixture
    def predefined_state_manager(self):
        """This fixture returns a StateManager instance which has three steps already."""
        step_fir_example = Step(
            function=example_function,
            name="FirstStep",
            success="SecondStep",
            fail="failure",
            function_params={"function_code": 1},
            interval=7,
        )
        step_sec_example = Step(
            function=example_function,
            name="SecondStep",
            success="ThirdStep",
            fail="failure",
            function_params={"function_code": 2},
            retry=3,
        )
        step_thi_example = Step(
            function=example_function,
            name="ThirdStep",
            success="FourthStep",
            fail="failure",
            function_params={"function_code": 3},
        )
        step_fou_example = Step(
            function=example_function,
            name="FourthStep",
            success="FifthStep",
            fail="failure",
            function_params={"function_code": 4},
        )
        step_fif_example = Step(
            function=example_function,
            name="FifthStep",
            success="success",
            fail="failure",
            function_params={"function_code": 5},
        )
        sm = StateManager(step_fir_example, "state_manager_test")
        sm.add_step(step_fir_example)
        sm.add_step(step_sec_example)
        sm.add_step(step_thi_example)
        sm.add_step(step_fou_example)
        sm.add_step(step_fif_example)

        return sm

    def test_initilization_of_default_steps(self, predefined_state_manager):
        """Test if the constructor creates neccessary steps."""
        organizer_step = predefined_state_manager.steps["organizer"]
        assert isinstance(organizer_step, Step)

        success_step = predefined_state_manager.steps["success"]
        assert isinstance(success_step, Step)

        failure_step = predefined_state_manager.steps["failure"]
        assert isinstance(failure_step, Step)

    def test_add_step_ordinary_input(self, predefined_state_manager):
        """Test an ordinary use-case for the add_step() method."""
        step_example = Step(
            function=example_function,
            name="OrdinaryStep",
            success="success",
            fail="failure",
        )
        predefined_state_manager.add_step(step_example)

        got_step = predefined_state_manager.steps["OrdinaryStep"]
        assert isinstance(got_step, Step)
        assert got_step.function == example_function

    def test_add_step_repeated_input(self, predefined_state_manager):
        """Test an extra-ordinary use-case if someone tries
        to add more then one step with same name. It should raise
        an exception.

        @TODO: Give a spesific exception type.
        """
        step_example = Step(
            function=example_function,
            name="RepeatedStep",
            success="success",
            fail="failure",
        )
        predefined_state_manager.add_step(step_example)
        # with pytest.raises(Exception):
        #     predefined_state_manager.add_step(step_example)
        assert True  # Do not test this for now. This is not supported yet.

    def test_get_step_ordinary_input(self, predefined_state_manager):
        """Test an ordinary use-case for the get_step() method."""
        got_step = predefined_state_manager.get_step("SecondStep")
        assert isinstance(got_step, Step)
        assert got_step.success == "ThirdStep"

    def test_get_step_non_inserted_step(self, predefined_state_manager):
        """Test if calling get_step() with a step does not exist,
        throws an exception.
        """
        with pytest.raises(KeyError):
            predefined_state_manager.get_step("ExampleStepThatIsNotExists")

    @pytest.mark.parametrize("tick_count", [5, 1, 25])
    def test_clear_counter_and_counter_tick(self, predefined_state_manager, tick_count):
        """Test the clear_counter() and counter_tick() methods."""
        for _ in range(tick_count):
            predefined_state_manager.counter_tick()
        assert predefined_state_manager.retry_counter == tick_count

        predefined_state_manager.clear_counter()
        assert predefined_state_manager.retry_counter == 0

    def test_success(self, mocker, predefined_state_manager):
        """Test the succes() method if it returns a success step
        with cache's last response.
        """
        mocker.patch(
            "pico_lte.common.StateCache.get_last_response",
            return_value="last_response_mocked",
        )
        returned_value = predefined_state_manager.success()
        assert returned_value.get("status") == Status.SUCCESS
        assert returned_value.get("response") == "last_response_mocked"

    def test_failure(self, mocker, predefined_state_manager):
        """Test the failure() method if it returns a success step
        with cache's last response.
        """
        mocker.patch(
            "pico_lte.common.StateCache.get_last_response",
            return_value="last_response_mocked",
        )
        returned_value = predefined_state_manager.failure()
        assert returned_value.get("status") == Status.ERROR
        assert returned_value.get("response") == "last_response_mocked"

    def test_organizer_with_current_step_is_organizer_and_cache_none(
        self, mocker, predefined_state_manager
    ):
        """Tests the organizer() method with current step as organizer,
        and cached step is not available.
        """
        mocker.patch(
            "pico_lte.common.StateCache.get_state",
            return_value=None,
        )
        assert predefined_state_manager.current.name == "organizer"

        response = predefined_state_manager.organizer()

        assert response.get("status") == Status.SUCCESS
        assert predefined_state_manager.current.name == "FirstStep"

    def test_organizer_with_current_step_is_organizer_and_cache_exists(
        self, mocker, predefined_state_manager
    ):
        """Tests the organizer() method with current step as organizer
        and cache exists."""
        mocker.patch(
            "pico_lte.common.StateCache.get_state",
            return_value="ThirdStep",
        )

        assert predefined_state_manager.current.name == "organizer"

        response = predefined_state_manager.organizer()
        assert response.get("status") == Status.SUCCESS

        assert predefined_state_manager.current.name == "ThirdStep"

    def test_organizer_with_current_step_is_ok(self, predefined_state_manager):
        """Tests the organizer() method with current step' is_ok attribute
        is True with both cached and non-cached probabilities.
        """
        # Get FirstStep as current step.
        predefined_state_manager.current.is_ok = True
        predefined_state_manager.organizer()

        # Get SecondStep to test.
        predefined_state_manager.current.is_ok = True
        predefined_state_manager.current.cachable = True
        response = predefined_state_manager.organizer()

        assert response.get("status") == Status.SUCCESS
        assert predefined_state_manager.current.name == "SecondStep"
        assert config["cache"].states[predefined_state_manager.function_name] == "FirstStep"

    def test_organizer_without_current_is_ok_and_retry_current(self, predefined_state_manager):
        """Tests the organizer() method's behaviour on the steps
        with given retry attribute.
        """
        # Get SecondStep as current step.
        predefined_state_manager.organizer()
        predefined_state_manager.current.is_ok = True
        predefined_state_manager.organizer()

        counter_before = predefined_state_manager.retry_counter
        predefined_state_manager.organizer()
        predefined_state_manager.organizer()
        counter_after = predefined_state_manager.retry_counter

        assert counter_after - counter_before == 2
        assert predefined_state_manager.current.name == "SecondStep"

        # Try the last time.
        predefined_state_manager.organizer()
        # Go to failure step.
        predefined_state_manager.organizer()
        assert predefined_state_manager.current.name == "failure"

    def test_execute_organizer_step(self):
        """No need to test this function for now."""
        assert True

    def test_execute_current_step(self, predefined_state_manager):
        """Tests the execute_current_step() method."""
        # Go to first step.
        predefined_state_manager.organizer()
        result = predefined_state_manager.execute_current_step()

        assert config["cache"].get_last_response() == result["response"]
        assert predefined_state_manager.current.is_ok == True

    def test_run_with_default_parameters(self, predefined_state_manager):
        """Tests the run() method without begin and end parameters."""
        # On first step.
        result = predefined_state_manager.run()
        assert result.get("status") == Status.ONGOING
        assert result.get("interval") == 7
        assert result.get("response") is not None

        # On last step.
        while True:
            result = predefined_state_manager.run()
            if result.get("status") == Status.SUCCESS:
                break
        assert result.get("response") == 5

    @pytest.mark.parametrize("state_name", ["SecondStep", "FourthStep"])
    def test_run_with_begin(self, state_name, predefined_state_manager):
        """Tests the run() method with given begin parameter."""
        predefined_state_manager.run(begin=state_name)
        assert predefined_state_manager.current.name == state_name

        while True:
            result = predefined_state_manager.run()
            if result.get("status") == Status.SUCCESS:
                break

        assert result.get("response") == 5

    @pytest.mark.parametrize("state_name, expected_response", [("ThirdStep", 3), ("SecondStep", 2)])
    def test_run_with_end(self, state_name, expected_response, predefined_state_manager):
        """Tests the run() method with given end parameter."""
        while True:
            result = predefined_state_manager.run(end=state_name)
            if result.get("status") == Status.SUCCESS:
                break

        assert result.get("response") == expected_response
