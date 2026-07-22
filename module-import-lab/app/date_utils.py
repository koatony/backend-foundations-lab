from datetime import date


def calculate_days_between(day1_str:str, day2_str: str)-> int:
    """Calculate the number of days between two dates"""
    try:
        day1 = date.fromisoformat(day1_str)
        day2 = date.fromisoformat(day2_str)
    except ValueError as error:
        print(f"Please provide a valid date string. Error: {error}")
        return None
    delta = day2 - day1
    return abs(delta.days)


def show_name()->str:
    return __name__


