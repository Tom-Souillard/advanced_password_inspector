import hashlib
import requests
from zxcvbn import zxcvbn
from requests.exceptions import RequestException

def evaluate_password(password: str) -> dict:
    """
    Evaluate the strength and exposure of a given password using the zxcvbn library and Have I Been Pwned API.

    Args:
        password (str): The password to evaluate.

    Returns:
        dict: A dictionary containing the evaluation results for password strength, breach status, and crack time.
    """
    if not password:
        raise ValueError("Password must not be empty")

    # Evaluate password strength using zxcvbn
    strength_results = zxcvbn(password)

    # Check for password breaches
    breach_check = check_password_breach(password)

    # Estimate crack time
    crack_time = estimate_crack_time(strength_results)

    # Combine results into a dictionary
    results = {
        'password_strength': strength_results,
        'breach_check': breach_check,
        'crack_time': crack_time
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

    # Build the URL for the API request
    url = f'https://api.pwnedpasswords.com/range/{first5_char}'

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        # Process the response to find if the remainder of our hash is in the breached list
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == tail:
                return True
        return False
    except RequestException as e:
        print(f"Failed to check password breach: {e}")
        return None

def estimate_crack_time(zxcvbn_result: dict) -> str:
    """
    Estimate the time required to crack the password based on zxcvbn analysis.

    Args:
        zxcvbn_result (dict): The result from zxcvbn password strength analysis.

    Returns:
        str: A human-readable estimate of how long it would take to crack the password.
    """
    # Check if the necessary data exists in the results
    try:
        seconds = zxcvbn_result['crack_times_seconds']['offline_slow_hashing_1e4_per_second']
        if seconds < 60:
            return "instant"
        elif seconds < 3600:
            return "minutes"
        elif seconds < 86400:
            return "hours"
        elif seconds < 31536000:
            return "days"
        else:
            return "centuries"
    except KeyError:
        return "Data unavailable"
