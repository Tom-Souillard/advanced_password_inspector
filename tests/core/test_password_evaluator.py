import pytest
from src.core.password_evaluator import evaluate_password, check_password_breach, estimate_crack_time
from unittest.mock import patch, Mock
import requests

# Simulated responses for zxcvbn analysis
mock_zxcvbn_response_weak = {
    'score': 0,
    'feedback': {
        'warning': 'This is a top-10 common password.',
        'suggestions': ['Add another word or two. Uncommon words are better.']
    },
    'crack_times_seconds': {
        'offline_slow_hashing_1e4_per_second': 0.1
    }
}

mock_zxcvbn_response_strong = {
    'score': 3,
    'feedback': {
        'warning': '',
        'suggestions': ['Your password is strong.']
    },
    'crack_times_seconds': {
        'offline_slow_hashing_1e4_per_second': 2000000000
    }
}

@pytest.mark.parametrize("password, expected_score, expected_suggestion", [
    ("password123", 0, 'Add another word or two. Uncommon words are better.'),
    ("StrongPassword!2024", 3, 'Your password is strong.'),
    ("WeakPassword", 0, 'Add another word or two. Uncommon words are better.')
])
def test_evaluate_password_strength(password, expected_score, expected_suggestion):
    """Tests the password evaluation function to ensure it integrates zxcvbn analysis correctly."""
    with patch('src.core.password_evaluator.zxcvbn', return_value=mock_zxcvbn_response_weak if expected_score == 0 else mock_zxcvbn_response_strong) as mock_zxcvbn:
        result = evaluate_password(password)
        assert isinstance(result, dict), "The result should be a dictionary."
        assert 'password_strength' in result, "The result should include password strength analysis."
        assert result['password_strength']['score'] == expected_score, f"Expected score for '{password}' should be {expected_score}."
        assert result['password_strength']['feedback']['suggestions'][0] == expected_suggestion, f"Feedback suggestion does not match for '{password}'."

def test_evaluate_password_empty_input():
    """Tests the evaluate_password function with an empty input to ensure it raises a ValueError."""
    with pytest.raises(ValueError) as excinfo:
        evaluate_password("")
    assert str(excinfo.value) == "Password must not be empty"

@pytest.mark.parametrize("password, api_response, expected_result", [
    ("12345678", "FB2927D828AF22F592134E8932480637C0D:1", True),
    ("P@ssw0rd!", "00A4A8D501AA5A9902F3F7F8BD9560B1439:5", False)
])
def test_check_password_breach(password, api_response, expected_result):
    """Tests the check_password_breach function to ensure it detects breaches correctly."""
    mock_response = Mock()
    mock_response.text = api_response
    with patch('requests.get', return_value=mock_response):
        result = check_password_breach(password)
        assert result == expected_result, f"Expected {expected_result} for password '{password}' but got {result}."

def test_check_password_breach_connection_error():
    """Tests the check_password_breach function to ensure it handles connection errors by raising an error."""
    with patch('requests.get', side_effect=requests.exceptions.RequestException):
        with pytest.raises(RuntimeError) as excinfo:
            check_password_breach("testpassword")
        assert "API request failed" in str(excinfo.value)

@pytest.mark.parametrize("password, expected_time, strength", [
    ("123456", "instant", 'weak'),
    ("strongpassword12345!", "centuries", 'strong')
])
def test_estimate_crack_time(password, expected_time, strength):
    """Tests the estimate_crack_time function to ensure it provides accurate estimates."""
    with patch('src.core.password_evaluator.zxcvbn', return_value=mock_zxcvbn_response_weak if strength == 'weak' else mock_zxcvbn_response_strong):
        result = evaluate_password(password)
        assert result['crack_time'] == expected_time, f"Expected {expected_time}, got {result['crack_time']}"
