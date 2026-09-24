import logging
import sys
import math


log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/file_txt.log", encoding="utf-8")
    ]
)


def calculate_triangle(side_a, side_b, side_c):
    logging.info(
        f"Получены стороны: A={side_a}, B={side_b}, C={side_c}"
    )

    try:
        a = float(side_a)
        b = float(side_b)
        c = float(side_c)

        logging.debug(f"Преобразованные значения: {a}, {b}, {c}")

        if a <= 0 or b <= 0 or c <= 0:
            logging.error("Стороны должны быть положительными числами")
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

        if a + b <= c or a + c <= b or b + c <= a:
            logging.warning("Из данных сторон нельзя составить треугольник")
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

        logging.info(f"Тип треугольника: {triangle_type}")
        logging.info(f"Координаты вершин: {coordinates}")

        return triangle_type, coordinates

    except (ValueError, TypeError) as error:
        logging.error("Некорректные входные данные")
        logging.exception(error)

        return "", [(-2, -2), (-2, -2), (-2, -2)]


def main():
    logging.info("Программа запущена")

    side_a = input("Введите сторону A: ")
    side_b = input("Введите сторону B: ")
    side_c = input("Введите сторону C: ")

    triangle_type, coordinates = calculate_triangle(
        side_a,
        side_b,
        side_c
    )

    print("\nТип треугольника:", triangle_type)
    print("Координаты вершин:", coordinates)

    logging.info("Программа завершена")


if __name__ == "__main__":
    main()