import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.my_project import calculate_triangle


class TestTriangleValidation(unittest.TestCase):
    """Тесты валидации входных данных."""

    def test_negative_side_returns_not_triangle(self):
        """Отрицательная сторона → 'не треугольник' и координаты (-1, -1)."""
        result, coords = calculate_triangle(-3, 4, 5)
        self.assertEqual(result, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_zero_side_returns_not_triangle(self):
        """Нулевая сторона → 'не треугольник' и координаты (-1, -1)."""
        result, coords = calculate_triangle(0, 4, 5)
        self.assertEqual(result, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_non_numeric_string_returns_empty_type(self):
        """Строка 'abc' не преобразуется в число → пустой тип и координаты (-2, -2)."""
        result, coords = calculate_triangle("abc", 4, 5)
        self.assertEqual(result, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_none_value_returns_empty_type(self):
        """None не преобразуется в число → пустой тип и координаты (-2, -2)."""
        result, coords = calculate_triangle(None, 4, 5)
        self.assertEqual(result, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])


class TestTriangleInequality(unittest.TestCase):
    """Тесты неравенства треугольника."""

    def test_sum_equals_third_side_is_not_triangle(self):
        """1 + 2 == 3 → вырожденный треугольник недопустим."""
        result, coords = calculate_triangle(1, 2, 3)
        self.assertEqual(result, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_sum_less_than_third_side_is_not_triangle(self):
        """2 + 3 < 10 → треугольника не существует."""
        result, coords = calculate_triangle(2, 3, 10)
        self.assertEqual(result, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])


class TestTriangleTypes(unittest.TestCase):
    """Тесты определения типа треугольника."""

    def test_equilateral_triangle_type(self):
        """5, 5, 5 → равносторонний."""
        result, _ = calculate_triangle(5, 5, 5)
        self.assertEqual(result, "равносторонний")

    def test_isosceles_triangle_type(self):
        """5, 5, 7 → равнобедренный."""
        result, _ = calculate_triangle(5, 5, 7)
        self.assertEqual(result, "равнобедренный")

    def test_scalene_triangle_type(self):
        """3, 4, 5 → разносторонний."""
        result, _ = calculate_triangle(3, 4, 5)
        self.assertEqual(result, "разносторонний")

    def test_float_sides_equilateral(self):
        """2.5, 2.5, 2.5 → равносторонний (проверка работы с float)."""
        result, _ = calculate_triangle(2.5, 2.5, 2.5)
        self.assertEqual(result, "равносторонний")


class TestTriangleCoordinates(unittest.TestCase):
    """Тесты возвращаемых координат."""

    def test_first_vertex_is_origin(self):
        """Первая вершина всегда в (0, 0)."""
        _, coords = calculate_triangle(3, 4, 5)
        self.assertEqual(coords[0], (0, 0))

    def test_second_vertex_on_x_axis(self):
        """Вторая вершина лежит на оси X: y=0 и x>0."""
        _, coords = calculate_triangle(3, 4, 5)
        self.assertEqual(coords[1][1], 0)
        self.assertGreater(coords[1][0], 0)

    def test_coordinates_are_integers(self):
        """Все координаты — целые числа."""
        _, coords = calculate_triangle(3, 4, 5)
        for x, y in coords:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)


if __name__ == "__main__":
    unittest.main()