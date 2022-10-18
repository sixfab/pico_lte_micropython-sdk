"""
Test module for the utils.status module.
"""

from core.utils.status import Status

class TestStatus:
    """
    Test class for the utils.status module.
    """

    def test_status_codes(self):
        """This method tests the attributes of Status class.
        """
        assert Status.SUCCESS == 0
        assert Status.ERROR == 1
        assert Status.TIMEOUT == 2
        assert Status.ONGOING == 3
        assert Status.UNKNOWN == 99
