import logging
import sys
import os

from calculator import TriangleCalculator
from database import TriangleDatabase
from user_interface import ConsoleUserInterface
from notifier import EmailNotifier
from controller import Controller


log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/file_txt.log", encoding="utf-8")
    ]
)


def main():
    logging.info("Программа запущена")

    calculator = TriangleCalculator()
    database = TriangleDatabase("triangles.db")
    user_interface = ConsoleUserInterface()
    notifier = EmailNotifier()

    controller = Controller(calculator, database, user_interface, notifier)

    triangle_type, coordinates = controller.run()

    print("\nТип треугольника:", triangle_type)
    print("Координаты вершин:", coordinates)

    database.close()
    logging.info("Программа завершена")


if __name__ == "__main__":
    main()