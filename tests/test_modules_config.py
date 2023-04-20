"""
Test module for the modules.config module.
"""

import pytest

from pico_lte.modules.config import Config
from pico_lte.common import config


class TestConfig:
    """
    Test class for Config.
    """

    @pytest.fixture
    def config_instance(self):
        """This fixture returns a Config instance."""
        return Config()

    @pytest.fixture
    def example_config_params(self):
        """This fixture returns an example Config.params."""
        return {
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
        }

    def test_set_parameters(self, config_instance, example_config_params):
        """This method tests the set_parameters() method."""
        config_instance.set_parameters(example_config_params)
        assert config["params"] == example_config_params

    def test_read_parameters_from_json_file(self, mocker, config_instance, example_config_params):
        """This method tests the read_parameters_from_json_file() method."""
        mocker.patch("pico_lte.modules.config.read_json_file", return_value=example_config_params)

        config_instance.read_parameters_from_json_file("some_path.json")
        assert config["params"] == example_config_params
