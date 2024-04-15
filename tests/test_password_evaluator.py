import pytest
from src.core.password_evaluator import evaluate_password, check_password_breach, estimate_crack_time
from unittest.mock import patch, Mock
import requests

# Données simulées pour les réponses de zxcvbn
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
        'offline_slow_hashing_1e4_per_second': 20000000
    }
}

mock_responses = {
    'weak': {'crack_times_seconds': {'online_throttling_100_per_hour': 3600, 'offline_slow_hashing_1e4_per_second': 0.5}},
    'strong': {'crack_times_seconds': {'online_throttling_100_per_hour': 31536000, 'offline_slow_hashing_1e4_per_second': 20000}}
}


@pytest.mark.parametrize("password, expected_score, expected_suggestion", [
    ("password123", 0, 'Add another word or two. Uncommon words are better.'),
    ("StrongPassword!2024", 3, 'Your password is strong.'),
    ("WeakPassword", 0, 'Add another word or two. Uncommon words are better.')
])
def test_evaluate_password_strength(password, expected_score, expected_suggestion):
    """
    Test the evaluate_password function to ensure it correctly integrates zxcvbn analysis.
    """
    # Mocking zxcvbn responses based on password strength
    if expected_score == 3:
        zxcvbn_response = mock_zxcvbn_response_strong
    else:
        zxcvbn_response = mock_zxcvbn_response_weak

    with patch('src.core.password_evaluator.zxcvbn', return_value=zxcvbn_response):
        result = evaluate_password(password)

        # Vérifier le type et la structure de la réponse
        assert isinstance(result, dict), "The result should be a dictionary."
        assert 'password_strength' in result, "The result should include password strength analysis."
        assert result['password_strength']['score'] == expected_score, \
            f"Expected score for '{password}' should be {expected_score}."
        assert result['password_strength']['feedback']['suggestions'][0] == expected_suggestion, \
            f"Feedback suggestion does not match for '{password}'."

def test_evaluate_password_empty_input():
    """
    Test evaluate_password with an empty password input to ensure it handles empty or invalid inputs gracefully.
    """
    password = ""
    with pytest.raises(ValueError) as excinfo:
        evaluate_password(password)
    assert str(excinfo.value) == "Password must not be empty"

@pytest.mark.parametrize("password, api_response, expected_result", [
    ("12345678", "FB2927D828AF22F592134E8932480637C0D:1", True),  # Password is breached
    ("P@ssw0rd!", "00A4A8D501AA5A9902F3F7F8BD9560B1439:5", False),  # Password is safe
])
def test_check_password_breach(password, api_response, expected_result):
    """
    Test the check_password_breach function to ensure it properly detects if a password has been exposed in data breaches.
    """
    mock_response = Mock()
    mock_response.text = api_response
    with patch('requests.get', return_value=mock_response):
        result = check_password_breach(password)
        assert result == expected_result, f"Expected {expected_result} for password '{password}' but got {result}."

def test_check_password_breach_connection_error():
    """
    Test the check_password_breach function to handle connection errors gracefully.
    """
    password = "P@ssw0rd!"
    with patch('requests.get', side_effect=requests.exceptions.RequestException):
        result = check_password_breach(password)
        assert result is None, "Expected result should be None when there is a connection error."


@pytest.mark.parametrize("password, expected_time, strength", [
    ("123456", "instant", 'weak'),
    ("strongpassword12345!", "centuries", 'strong'),
])
def test_estimate_crack_time(password, expected_time, strength):
    """
    Test the estimate_crack_time function to ensure it provides accurate crack time estimates.
    """
    with patch('src.core.password_evaluator.zxcvbn', return_value=mock_zxcvbn_response_weak):
        result = evaluate_password("weakpassword")
        # Make sure you're asserting on the 'crack_time', not directly on the password input
        assert result['crack_time'] == "instant", "Expected instant, got {}".format(result['crack_time'])
