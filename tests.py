import unittest
from unittest.mock import patch, MagicMock

from calculator import TriangleCalculator
from database import TriangleDatabase
from user_interface import ConsoleUserInterface, UserInterface
from notifier import EmailNotifier, Notifier
from controller import Controller


# ============================================================
# ЮНИТ-ТЕСТЫ КЛАССА ВЫЧИСЛЕНИЙ
# ============================================================

class TestCalculator(unittest.TestCase):
    """Юнит-тесты для класса вычислений (все ветки)."""

    def setUp(self):
        self.calc = TriangleCalculator()

    def test_equilateral_triangle(self):
        triangle_type, coords = self.calc.calculate(5, 5, 5)
        self.assertEqual(triangle_type, "равносторонний")
        self.assertEqual(len(coords), 3)

    def test_isosceles_triangle(self):
        triangle_type, coords = self.calc.calculate(5, 5, 8)
        self.assertEqual(triangle_type, "равнобедренный")

    def test_scalene_triangle(self):
        triangle_type, coords = self.calc.calculate(3, 4, 5)
        self.assertEqual(triangle_type, "разносторонний")

    def test_negative_side(self):
        triangle_type, coords = self.calc.calculate(-1, 4, 5)
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_zero_side(self):
        triangle_type, coords = self.calc.calculate(0, 4, 5)
        self.assertEqual(triangle_type, "не треугольник")

    def test_triangle_inequality_fails(self):
        triangle_type, coords = self.calc.calculate(1, 2, 10)
        self.assertEqual(triangle_type, "не треугольник")

    def test_non_numeric_input(self):
        triangle_type, coords = self.calc.calculate("a", "b", "c")
        self.assertEqual(triangle_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_string_numbers_are_accepted(self):
        triangle_type, coords = self.calc.calculate("3", "4", "5")
        self.assertEqual(triangle_type, "разносторонний")


# ============================================================
# ЮНИТ-ТЕСТЫ КЛАССА БАЗЫ ДАННЫХ
# ============================================================

class TestDatabase(unittest.TestCase):
    """Юнит-тесты для класса БД (add / get / delete / close)."""

    def setUp(self):
        self.db = TriangleDatabase(":memory:")

    def tearDown(self):
        try:
            self.db.close()
        except Exception:
            pass

    def test_add_and_get_record(self):
        self.db.add_record("3", "4", "5", "разносторонний", "[(0,0)]")
        record = self.db.get_record("3", "4", "5")
        self.assertIsNotNone(record)
        self.assertEqual(record["triangle_type"], "разносторонний")

    def test_get_missing_record_returns_none(self):
        record = self.db.get_record("99", "99", "99")
        self.assertIsNone(record)

    def test_delete_record(self):
        self.db.add_record("3", "4", "5", "разносторонний", "[(0,0)]")
        self.db.delete_record("3", "4", "5")
        record = self.db.get_record("3", "4", "5")
        self.assertIsNone(record)

    def test_add_record_overwrites_existing(self):
        self.db.add_record("3", "4", "5", "разносторонний", "[(0,0)]")
        self.db.add_record("3", "4", "5", "равнобедренный", "[(1,1)]")
        record = self.db.get_record("3", "4", "5")
        self.assertEqual(record["triangle_type"], "равнобедренный")

    def test_close_connection(self):
        self.db.close()
        # после закрытия курсор должен ругаться при попытке работы
        with self.assertRaises(Exception):
            self.db.cursor.execute("SELECT 1")


# ============================================================
# ЮНИТ-ТЕСТЫ КЛАССА ПОЛЬЗОВАТЕЛЬСКОГО ВВОДА
# ============================================================

class TestConsoleUserInterface(unittest.TestCase):
    """Юнит-тесты класса взаимодействия с пользователем."""

    @patch("builtins.input", side_effect=["3", "4", "5"])
    def test_get_input_returns_three_values(self, mock_input):
        ui = ConsoleUserInterface()
        result = ui.get_input()
        self.assertEqual(result, ("3", "4", "5"))
        self.assertEqual(mock_input.call_count, 3)

    def test_user_interface_is_abstract(self):
        with self.assertRaises(TypeError):
            UserInterface()  # нельзя инстанцировать абстрактный класс


# ============================================================
# ЮНИТ-ТЕСТЫ КЛАССА СТОРОННЕЙ ЗАВИСИМОСТИ
# ============================================================

class TestNotifier(unittest.TestCase):
    """Юнит-тесты класса-уведомителя (имитация внешнего сервера)."""

    def test_email_notifier_send_returns_true(self):
        notifier = EmailNotifier()
        result = notifier.send("тестовое сообщение")
        self.assertTrue(result)

    def test_notifier_is_abstract(self):
        with self.assertRaises(TypeError):
            Notifier()  # нельзя инстанцировать абстрактный класс


# ============================================================
# ИНТЕГРАЦИОННЫЕ ТЕСТЫ (минимум 3 — у нас 6)
# ============================================================

class TestIntegration(unittest.TestCase):
    """Интеграционные тесты связки Controller + Calculator + DB + UI + Notifier."""

    def setUp(self):
        self.calculator = TriangleCalculator()
        self.database = TriangleDatabase(":memory:")
        self.user_interface = ConsoleUserInterface()
        self.notifier = EmailNotifier()

    def tearDown(self):
        try:
            self.database.close()
        except Exception:
            pass

    # --- 1. Нет записи в БД -> вычисляем и сохраняем ---
    @patch("builtins.input", side_effect=["5", "5", "5"])
    def test_controller_computes_and_saves(self, mock_input):
        controller = Controller(
            self.calculator, self.database, self.user_interface, self.notifier
        )
        triangle_type, coords = controller.run()
        self.assertEqual(triangle_type, "равносторонний")
        record = self.database.get_record("5", "5", "5")
        self.assertIsNotNone(record)
        self.assertEqual(record["triangle_type"], "равносторонний")

    # --- 2. Запись есть в БД -> берём из БД, не вычисляем ---
    @patch("builtins.input", side_effect=["5", "5", "5"])
    def test_controller_takes_from_db_on_second_call(self, mock_input):
        self.database.add_record(
            "5", "5", "5", "равносторонний",
            "[(0, 0), (99, 0), (50, 86)]"
        )
        controller = Controller(
            self.calculator, self.database, self.user_interface, self.notifier
        )
        with patch.object(self.calculator, "calculate") as mock_calc:
            triangle_type, coords = controller.run()
            # калькулятор НЕ должен вызываться, если запись есть в БД
            mock_calc.assert_not_called()
        self.assertEqual(triangle_type, "равносторонний")

    # --- 3. Проверяем вызов отправки на внешний сервер ---
    @patch("builtins.input", side_effect=["3", "4", "5"])
    @patch.object(EmailNotifier, "send")
    def test_controller_sends_to_notifier(self, mock_send, mock_input):
        mock_send.return_value = True
        controller = Controller(
            self.calculator, self.database, self.user_interface, self.notifier
        )
        controller.run()
        self.assertTrue(mock_send.called)

    # --- 4. Невалидные данные (не треугольник) ---
    @patch("builtins.input", side_effect=["1", "2", "10"])
    def test_controller_invalid_triangle(self, mock_input):
        controller = Controller(
            self.calculator, self.database, self.user_interface, self.notifier
        )
        triangle_type, coords = controller.run()
        self.assertEqual(triangle_type, "не треугольник")

    # --- 5. Полный сценарий с MagicMock вместо notifier ---
    @patch("builtins.input", side_effect=["5", "5", "5"])
    def test_controller_full_scenario_with_mock_notifier(self, mock_input):
        mock_notifier = MagicMock()
        mock_notifier.send.return_value = True

        controller = Controller(
            self.calculator, self.database, self.user_interface, mock_notifier
        )
        triangle_type, coords = controller.run()

        self.assertEqual(triangle_type, "равносторонний")
        mock_notifier.send.assert_called_once()

    # --- 6. Заглушка user_interface через MagicMock ---
    def test_controller_with_mocked_user_interface(self):
        mock_ui = MagicMock()
        mock_ui.get_input.return_value = ("3", "4", "5")

        mock_notifier = MagicMock()
        mock_notifier.send.return_value = True

        controller = Controller(
            self.calculator, self.database, mock_ui, mock_notifier
        )
        triangle_type, coords = controller.run()

        self.assertEqual(triangle_type, "разносторонний")
        mock_ui.get_input.assert_called_once()
        mock_notifier.send.assert_called_once()

    # --- 7. Второй вызов: сначала вычисление, потом взятие из БД ---
    @patch("builtins.input", side_effect=["6", "6", "6", "6", "6", "6"])
    def test_controller_caches_result_in_db(self, mock_input):
        controller = Controller(
            self.calculator, self.database, self.user_interface, self.notifier
        )
        # первый вызов — вычисляет и пишет в БД
        type1, _ = controller.run()
        # второй вызов — берёт из БД
        type2, _ = controller.run()
        self.assertEqual(type1, type2)


if __name__ == "__main__":
    unittest.main()