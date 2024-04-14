import pytest
from src.core.password_evaluator import evaluate_password
from unittest.mock import patch

# Données simulées pour les réponses de zxcvbn
mock_zxcvbn_response_weak = {
    'score': 0,
    'feedback': {
        'warning': 'This is a top-10 common password.',
        'suggestions': ['Add another word or two. Uncommon words are better.']
    }
}

mock_zxcvbn_response_strong = {
    'score': 3,
    'feedback': {
        'warning': '',
        'suggestions': ['Your password is strong.']
    }
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
