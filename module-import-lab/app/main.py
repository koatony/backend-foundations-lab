from app.date_utils import calculate_days_between, show_name
from app.math_utils import calculate_circle_area


def main()->None:
    days = calculate_days_between("2025-10-01", "2025-10-05")
    area = calculate_circle_area(5)
    print(f"Days between: {days}")
    print(f"Area of circle: {area}")
    
    
    print(show_name())



if __name__ == "__main__":
    main()