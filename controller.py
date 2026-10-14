import logging
import ast


class Controller:
    """Класс-контроллер, реализующий бизнес-логику."""

    def __init__(self, calculator, database, user_interface, notifier):
        self.calculator = calculator
        self.database = database
        self.user_interface = user_interface
        self.notifier = notifier

    def run(self):
        side_a, side_b, side_c = self.user_interface.get_input()

        record = self.database.get_record(side_a, side_b, side_c)

        if record is not None:
            logging.info("Запись найдена в БД, берём результат оттуда")
            triangle_type = record["triangle_type"]
            coordinates = ast.literal_eval(record["coordinates"])
        else:
            logging.info("Записи нет в БД, вычисляем результат")
            triangle_type, coordinates = self.calculator.calculate(
                side_a, side_b, side_c
            )
            self.database.add_record(
                side_a, side_b, side_c, triangle_type, coordinates
            )

        result_string = f"Тип треугольника: {triangle_type}, Координаты: {coordinates}"

        self.notifier.send(result_string)

        return triangle_type, coordinates