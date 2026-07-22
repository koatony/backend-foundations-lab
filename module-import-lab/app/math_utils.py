from math import pi


def calculate_circle_area(radius: float) -> float:
    """Calculate the area of a circle"""
    if radius <= 0:
        raise ValueError(f"Radius must be a positive number. radius is: {radius}")

    return pi * (radius ** 2)