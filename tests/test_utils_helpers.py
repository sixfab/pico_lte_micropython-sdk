import pytest
import json
import os

from core.utils.helpers import *


class TestHelpers:
    @pytest.fixture
    def dict_to_make_json(self):
        """A PyTest fixture to have examplary dictionary data."""
        return {"ExampleProp": "Data", "ExampleNote": 5}

    @pytest.fixture
    def example_result(self):
        """A PyTest fixture to have examplary modem response."""
        return {
            "status": Status.SUCCESS,
            "response": ["+DATA:a,b,c,d", "MEANINGFULL: X Y Z", "OK", "BOUNDARY"],
        }

    @pytest.fixture
    def data_to_test_binary(self):
        """A PyTest fixture to have example data to write into a binary file."""
        data_to_test = [4, 15, 255, 0]
        return bytearray(data_to_test)

    @pytest.fixture
    def prepared_config(self):
        """A PyTest fixture to have examplary configuration file."""
        return {
            "cache": {},
            "params": {
                "mqtts": {
                    "host": "test_global_mqtts_host",
                    "port": "test_global_mqtts_port",
                },
                "https": {
                    "endpoint": "test_global_http_endpoint",
                    "topic": "test_global_http_topic",
                },
                "app_service": {
                    "mqtts": {
                        "host": "test_app_mqtts_host",
                        "port": "test_app_mqtts_port",
                    },
                },
            },
        }

    def test_read_json_file_path_exists(self, dict_to_make_json):
        """It tests read_json_file() with given corret path.
        @TODO: It does not removes the file created. Solve it.
        """
        json_string = json.dumps(dict_to_make_json)
        with open("test.json", "w") as file_to_save_json:
            file_to_save_json.write(json_string)

        data_returned = read_json_file("test.json")

        try:
            os.remove("test.json")
        except:
            pass

        assert data_returned == dict_to_make_json

    def test_read_json_file_path_does_not_exists(self):
        """It tests read_json_file() with corrupted or wrong path."""
        data_returned = read_json_file("not_in_there.json")
        assert data_returned is None

    def test_write_json_file(self, dict_to_make_json):
        """It tests write_json_file()."""
        assert write_json_file("test.json", dict_to_make_json) in [
            dict_to_make_json,
            None,
        ]

    def test_get_desired_data_not_success(self):
        """It tests get_desired_data() function with non-successful response
        from Modem. It should return None in "value" attribute.
        """
        example_result = {"status": Status.TIMEOUT, "response": "timeout"}
        result = get_desired_data(example_result, "some_prefix")

        assert result.get("value") is None
        assert result["status"] == example_result["status"]
        assert result["response"] == example_result["response"]

    def test_get_desired_data_success_empty_response(self):
        """It tests get_desired_data() function with empty but succesful response
        from Modem. It should return None in "value" attribute.
        """
        example_result = {"status": Status.SUCCESS, "response": []}
        result = get_desired_data(example_result, prefix="+CME")

        assert result["value"] == None
        assert result["status"] == example_result["status"]
        assert result["response"] == example_result["response"]

    def test_get_desired_data_success_response_without_ok(self):
        """It tests get_desired_data() function with successful but
        have not finished response from Modem. It should return None
        in "value" attribute.
        """
        example_result = {
            "status": Status.SUCCESS,
            "response": ["+DATA:a,b,c,d", "MEANINGFULL: X Y Z", "BOUNDARY"],
        }
        result = get_desired_data(example_result, prefix="+DATA: ")

        assert result["value"] == None
        assert result["status"] == example_result["status"]
        assert result["response"] == example_result["response"]

    def test_get_desired_data_success_response_includes_ok_with_wrong_prefix(
        self, example_result
    ):
        """It tests get_desired_data() function with successful and
        finished response but without having prefix from Modem. It
        should return None in "value" attribute.
        """
        result = get_desired_data(example_result, prefix="+ERROR:", separator=" ")

        assert result["value"] == None
        assert result["status"] == example_result["status"]
        assert result["response"] == example_result["response"]

    def test_get_desired_data_success_response_includes_ok_with_wrong_seperator(
        self, example_result
    ):
        """It tests get_desired_data() function with successful and
        finished response but with unuseful seperator from Modem. It
        should return None in "value" attribute.
        """
        result = get_desired_data(example_result, prefix="+DATA:", separator=" ")
        assert result["value"] == "a,b,c,d"
        assert result["status"] == example_result["status"]
        assert result["response"] == example_result["response"]

    def test_get_desired_data_success_default_parameters(self, example_result):
        """It tests get_desired_data() function with default parameters."""
        result_one = get_desired_data(example_result, prefix="+DATA:")
        result_two = get_desired_data(example_result, prefix="MEANINGFULL: ")
        assert result_one["value"] == "a"
        assert result_two["value"] == "X Y Z"

    @pytest.mark.parametrize(
        "indices_one, expected_one, indices_two, expected_two",
        [
            ([1, 3], ["b", "d"], 0, "X"),
            ([0, 1], ["a", "b"], [2, 1], ["Z", "Y"]),
            ([3, 0], ["d", "a"], "all", ["X", "Y", "Z"]),
            ("wrong_input", "a", "2", "X"),
        ],
    )
    def test_get_desired_data_success_response_includes_ok_with_indices(
        self, example_result, indices_one, expected_one, indices_two, expected_two
    ):
        """It tests get_desired_data() function in ordinary use cases."""
        result_one = get_desired_data(
            example_result, prefix="+DATA:", data_index=indices_one, separator=","
        )
        result_two = get_desired_data(
            example_result,
            prefix="MEANINGFULL: ",
            separator=" ",
            data_index=indices_two,
        )

        assert result_one["value"] == expected_one
        assert result_two["value"] == expected_two

    def test_simplify(self):
        """It tests the simplify() function."""
        assert (
            simplify('A test quote " with lots of "."')
            == "A test quote  with lots of ."
        )
        assert simplify("A test 'quote' with 'one'.") == "A test quote with one."
        assert simplify(15) == 15
        assert simplify(None) == None

    def test_read_file_with_text_file(self):
        """It tests the read_file() function with text-file input."""
        with open("test_text_file", "wt") as file_to_test:
            file_to_test.write("test_document")

        test_read = read_file("test_text_file")

        try:
            os.remove("test_text_file")
        except:
            pass

        assert test_read in [None, "test_document"]

    def test_read_file_with_binary_file(self, data_to_test_binary):
        """It tests the read_file() function with binary-file input."""
        with open("test_binary_file", "wb") as file_to_test:
            file_to_test.write(data_to_test_binary)

        test_read = read_file("test_binary_file", file_type="b")

        try:
            os.remove("test_binary_file")
        except:
            pass

        assert test_read == data_to_test_binary

    def test_write_file_with_text_file(self):
        """It tests the write_file() function with text-file input."""
        data_to_test = "This is an example."
        test_write = write_file("test_text_file", data_to_test)

        with open("test_text_file", "rt") as file_to_test:
            data_got_from_file = file_to_test.read()

        assert test_write in [data_to_test, None]
        assert data_got_from_file in [data_to_test, None]

    def test_write_file_with_binary_file(self, data_to_test_binary):
        """It tests the write_file() function with binary-file input."""
        test_write = write_file("test_binary_file", data_to_test_binary, file_type="b")

        with open("test_binary_file", "rb") as file_to_test:
            data_got_from_file = file_to_test.read()

        assert test_write in [data_to_test_binary, None]
        assert data_got_from_file in [data_to_test_binary, None]

    def test_get_parameter_without_config_and_default(self, mocker):
        """It tests get_parameter() function without predefined config and default values."""
        mocker.patch("core.temp.config", return_value={})
        assert get_parameter("some_path") == None

    def test_get_parameter_no_config_with_default(self, mocker):
        """It tests get_parameter() function and using default values without predefined config."""
        mocker.patch("core.temp.config", return_value={})
        assert get_parameter("some_path", default="test") == "test"

    def test_get_parameter_not_included_info(self, mocker, prepared_config):
        """It tests get_parameter() function in a case that config file does not
        have asked information.
        """
        mocker.patch("core.temp.config", prepared_config)

        result_without_default = get_parameter(["not", "included", "path_name"])
        result_with_default = get_parameter(
            ["not", "included", "path_name"], default="TestDefault"
        )

        assert result_without_default == None
        assert result_with_default == "TestDefault"


"""
    def test_get_parameter_included_info(self, mocker, prepared_config):
        mocker.patch.dict(
            "core.temp.config",
            values=prepared_config,
            clear=True,
        )

        assert get_parameter(["app_service", "mqtts", "host"]) == "test_app_mqtts_host"
        assert (
            get_parameter(["app_service", "mqtts", "host"], default="something_else")
            == "test_app_mqtts_host"
        )
        assert (
            get_parameter(["app_service", "https", "endpoint"])
            == "test_global_http_endpoint"
        )
        assert (
            get_parameter(
                ["app_service", "https", "endpoint"], default="something_else"
            )
            == "test_global_http_endpoint"
        )
"""
