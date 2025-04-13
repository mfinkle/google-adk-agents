import datetime

def get_weather(zipcode: str) -> dict:
    """
    Returns the weather for the given zipcode.
    Args:
        zipcode (str): The zipcode for which to retrieve the weather.

    Returns:
        dict: temperature and conditions or error msg.
    
    Example:
        >>> get_weather(zipcode='90120')
        {'status': 'success', 'temperature': '75 F', 'conditions': 'Sunny'}
    """

    return {
        'status': 'success',
        'temperature': '75 F',
        'conditions': 'Sunny'
    }


def get_zipcode(location: str) -> dict:
    """Returns the zipcode for the given location.
    Args:
        location (str): The location or city for which to retrieve the zipcode.
    Returns:
        dict: zipcode or error msg.
        
    Example:
        >>> get_zipcode(location='Beverly Hills')
        {'status': 'success', 'zipcode': '90210'}
    """
    return {
        'status': 'success',
        'zipcode': '90210'
    }


def get_current_location() -> dict:
    """Returns the current location of the user.
    Returns:
        dict: location or error msg.
        
    Example:
        >>> get_current_location()
        {'status': 'success', 'location': 'Springfield, IL'}
    """
    return {
        'status': 'success',
        'location': 'Springfield, IL'
    }


def get_datetime() -> dict:
    """Returns the current date and time.
    Returns:
        dict: date and time or error msg.
        
    Example:
        >>> get_datetime()
        {'status': 'success', 'date': '2025-04-12', 'time': '10:30 AM'}
    """
    now = datetime.datetime.now()
    return {
        'status': 'success',
        'date': now.strftime('%Y-%m-%d'),
        'time': now.strftime('%I:%M %p')
    }


def calculate(expression: str) -> dict:
    """Calculates the given mathematical expression using Python eval limited to __builtins__.
    Args:
        expression (str): The mathematical expression to calculate.
    Returns:
        dict: result and status.
        
    Example:
        >>> calculate('2 + 2')
        {'result': 4, 'status': 'success'}
    """
    try:
        result = eval(expression, {'__builtins__': {}}, {})
        return { 'result': result, 'status': 'success' }
    except (SyntaxError, NameError, TypeError, ZeroDivisionError) as e:
        return { 'result': None, 'status': 'fail' }
