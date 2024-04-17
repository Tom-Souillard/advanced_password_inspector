import hashlib
import requests
from zxcvbn import zxcvbn
from requests.exceptions import RequestException
from functools import lru_cache
from typing import Dict, Union

def evaluate_password(password: str) -> Dict[str, Union[dict, bool, str]]:
    """
    Evaluate the strength, breach status, and crack time estimation of a given password.

    Args:
        password (str): The password to evaluate.

    Returns:
        Dict[str, Union[dict, bool, str]]: A dictionary containing evaluation results:
            - 'password_strength' (dict): Results from zxcvbn analysis.
            - 'breach_check' (bool): True if the password is found in breach databases, False otherwise.
            - 'crack_time' (str): Human-readable estimate of how long it would take to crack the password.

    Raises:
        ValueError: If the password is empty.
    """
    if not password:
        raise ValueError("Password must not be empty")

    strength_results = zxcvbn(password)
    breach_check = check_password_breach(password)
    crack_time = estimate_crack_time(strength_results)

    return {
        'password_strength': strength_results,
        'breach_check': breach_check,
        'crack_time': crack_time
    }

@lru_cache(maxsize=1024)
def check_password_breach(password: str) -> Union[bool, None]:
    """
    Check if a password has been exposed in known data breaches using the Have I Been Pwned API.

    Args:
        password (str): The password to check.

    Returns:
        bool: True if the password is found in the breach databases, False otherwise.
        None: If the API request fails.

    Raises:
        RuntimeError: If the API request fails due to connection issues.
    """
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    url = f'https://api.pwnedpasswords.com/range/{first5_char}'

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return tail in (line.split(':')[0] for line in response.text.splitlines())
    except RequestException as e:
        raise RuntimeError(f"API request failed: {e}")

def estimate_crack_time(zxcvbn_result: dict) -> str:
    """
    Estimate the time required to crack the password based on zxcvbn analysis.

    Args:
        zxcvbn_result (dict): The result from zxcvbn password strength analysis.

    Returns:
        str: A human-readable estimate of how long it would take to crack the password, e.g., 'instant', 'minutes', 'hours', 'days', or 'centuries'.

    Raises:
        KeyError: If the necessary data is not found in the zxcvbn result.
    """
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
