from datetime import datetime

def get_current_time():
    """
    Returns the current local time as a string.
    """
    return datetime.now().strftime("%I:%M:%S %p")