from zxcvbn import zxcvbn

def evaluate_password(password: str) -> dict:
    """
    Evaluate the strength of a given password using the zxcvbn library.

    Args:
        password (str): The password to evaluate.

    Returns:
        dict: A dictionary containing the evaluation results for password strength.
    """
    if not password:
        raise ValueError("Password must not be empty")

    # Evaluate password strength using zxcvbn
    strength_results = zxcvbn(password)

    # Prepare the results dictionary to include only zxcvbn evaluation results
    results = {
        'password_strength': strength_results
    }

    return results
