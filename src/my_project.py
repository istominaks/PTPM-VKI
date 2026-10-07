import math


def calculate_triangle(side_a, side_b, side_c):
    try:
        a = float(side_a)
        b = float(side_b)
        c = float(side_c)

        if a <= 0 or b <= 0 or c <= 0:
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

        if a + b <= c or a + c <= b or b + c <= a:
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

        if a == b == c:
            triangle_type = "равносторонний"
        elif a == b or a == c or b == c:
            triangle_type = "равнобедренный"
        else:
            triangle_type = "разносторонний"

        x1 = 0
        y1 = 0

        scale = 99 / max(a, b, c)

        a_scaled = a * scale
        b_scaled = b * scale
        c_scaled = c * scale

        x2 = int(round(a_scaled))
        y2 = 0

        x3 = int(round(
            (b_scaled * b_scaled + a_scaled * a_scaled - c_scaled * c_scaled)
            / (2 * a_scaled)
        ))

        y3_value = b_scaled * b_scaled - x3 * x3

        if y3_value < 0:
            y3 = 0
        else:
            y3 = int(round(math.sqrt(y3_value)))

        coordinates = [
            (x1, y1),
            (x2, y2),
            (x3, y3)
        ]

        return triangle_type, coordinates

    except (ValueError, TypeError):
        return "", [(-2, -2), (-2, -2), (-2, -2)]