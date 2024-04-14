import hashlib
import requests
from zxcvbn import zxcvbn
from requests.exceptions import RequestException

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

    # Check for password breaches
    breach_check = check_password_breach(password)

    # Combine results into a dictionary
    results = {
        'password_strength': strength_results,
        'breach_check': breach_check
    }

    return results

def check_password_breach(password: str) -> bool:
    """
    Check if the password has been exposed in known data breaches using the Have I Been Pwned API.

    Args:
        password (str): The password to check.

    Returns:
        bool: True if the password is found in breach databases, False otherwise, or None if the check fails.
    """
    # Hash the password using SHA-1
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    # Get the first 5 characters of the hash to use with the API
    first5_char = sha1password[:5]
    tail = sha1password[5:]
    print(tail)
    # Build the URL for the API request
    url = f'https://api.pwnedpasswords.com/range/{first5_char}'

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raises HTTPError for bad responses

        # Process the response to find if the remainder of our hash is in the breached list
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == tail:
                return True  # The password was found in the breaches
        return False  # The password was not found
    except RequestException as e:
        # Log this error or handle it in a way that does not throw an exception
        print(f"Failed to check password breach: {e}")
        return None  # Indicate that the check could not be completed
