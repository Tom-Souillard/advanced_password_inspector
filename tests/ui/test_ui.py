import pytest
from unittest.mock import patch
from requests import RequestException
from advanced_password_inspector.core.password_evaluator import evaluate_password, check_password_breach, \
    estimate_crack_time

# Test data setup for different password scenarios
test_data = [
    ("weakpassword", {"score": 1, "feedback": {"suggestions": ["Use a few more characters."]},
                      "crack_times_seconds": {"offline_slow_hashing_1e4_per_second": 0.5}}, True, "instant"),
    ("StrongerPassword1234!", {"score": 3, "feedback": {"suggestions": []},
                               "crack_times_seconds": {"offline_slow_hashing_1e4_per_second": 31536000}}, False,
     "centuries")
]


@pytest.mark.parametrize("password, zxcvbn_result, breach_status, expected_crack_time", test_data)
def test_evaluate_password(password, zxcvbn_result, breach_status, expected_crack_time):
    """
    Test the evaluate_password function to ensure it correctly integrates zxcvbn analysis, breach check, and crack time estimation.
    """
    with patch('advanced_password_inspector.core.password_evaluator.zxcvbn', return_value=zxcvbn_result), \
        patch('advanced_password_inspector.core.password_evaluator.check_password_breach', return_value=breach_status), \
        patch('advanced_password_inspector.core.password_evaluator.estimate_crack_time',
              return_value=expected_crack_time):
        result = evaluate_password(password)
        assert result[
                   'password_strength'] == zxcvbn_result, "The password strength evaluation did not match expected results."
        assert result['breach_check'] == breach_status, "The breach check status did not match expected results."
        assert result['crack_time'] == expected_crack_time, "The crack time did not match expected results."


def test_evaluate_password_empty_input():
    """
    Test evaluate_password with an empty password input to ensure it raises a ValueError.
    """
    with pytest.raises(ValueError) as excinfo:
        evaluate_password("")
    assert str(excinfo.value) == "Password must not be empty", "Expected ValueError for empty password input."


def test_check_password_breach_connection_error():
    """
    Test the check_password_breach function to handle connection errors gracefully.
    """
    with patch('advanced_password_inspector.core.password_evaluator.requests.get', side_effect=RequestException("Connection error")), \
            pytest.raises(RuntimeError) as excinfo:
        check_password_breach("any_password")
    assert "API request failed: Connection error" in str(excinfo.value), "Expected a RuntimeError when the API request fails due to a connection error."
