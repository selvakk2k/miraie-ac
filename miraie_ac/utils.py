# Write a function check if the given string is a valid email address.

import re


def is_valid_email(addr):
    if re.match(r"^[0-9a-zA-Z\.\_]+\@[0-9a-zA-Z]+\.[0-9a-zA-Z]+$", addr):
        return True
    else:
        return False


def toFloat(value: str) -> float:
    if value is None:
        return -1.0
    try:
        return float(value)
    except ValueError:
        return -1.0


def toRoomTemp(value: str) -> float:
    """Parse the room temperature (rmtmp) from a status payload.

    Panasonic ACs report room temperatures in 0.5 degree steps, so a valid
    fractional part is only 0.0 or 0.5. On some newer firmware, the rmtmp value
    is encoded with unknown data before the actual room temperature,
    e.g. 150.27 -> 27, 2.29 -> 29, 61.26 -> 26. So when the value carries a
    fractional part that is neither zero nor 0.5, that decimal points to the
    actual room temperature.
    """
    temp = toFloat(value)
    if temp == -1.0:
        return temp
    fractional = temp - int(temp)
    if fractional != 0 and fractional != 0.5:
        # The decimal points to the actual room temperature.
        return float(round(fractional * 100))
    return temp
