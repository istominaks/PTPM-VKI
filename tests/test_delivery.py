import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.delivery_service import calculate_delivery_cost


class TestDeliveryValidation(unittest.TestCase):
    """Тесты валидации входных параметров."""

    def test_weight_below_minimum_returns_error(self):
        """Вес меньше 0.1 кг → ошибка."""
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual((cost, date), (-1, "0000-00-00"))

    def test_weight_above_maximum_returns_error(self):
        """Вес больше 50 кг → ошибка."""
        cost, date = calculate_delivery_cost(51, 100, "обычный")
        self.assertEqual((cost, date), (-1, "0000-00-00"))

    def test_distance_below_minimum_returns_error(self):
        """Дистанция меньше 1 км → ошибка."""
        cost, date = calculate_delivery_cost(1, 0, "обычный")
        self.assertEqual((cost, date), (-1, "0000-00-00"))

    def test_distance_above_maximum_returns_error(self):
        """Дистанция больше 5000 км → ошибка."""
        cost, date = calculate_delivery_cost(1, 5001, "обычный")
        self.assertEqual((cost, date), (-1, "0000-00-00"))

    def test_invalid_package_type_returns_error(self):
        """Неизвестный тип посылки → ошибка."""
        cost, date = calculate_delivery_cost(1, 100, "неизвестный")
        self.assertEqual((cost, date), (-1, "0000-00-00"))

    def test_boundary_weight_minimum_is_valid(self):
        """Вес ровно 0.1 кг — допустим (нижняя граница включительно)."""
        cost, date = calculate_delivery_cost(0.1, 100, "обычный")
        self.assertNotEqual(cost, -1)
        self.assertNotEqual(date, "0000-00-00")

    def test_boundary_weight_maximum_is_valid(self):
        """Вес ровно 50.0 кг — допустим (верхняя граница включительно)."""
        cost, date = calculate_delivery_cost(50.0, 100, "обычный")
        self.assertNotEqual(cost, -1)
        self.assertNotEqual(date, "0000-00-00")


class TestDeliveryCost(unittest.TestCase):
    """Тесты расчёта стоимости доставки."""

    def test_base_cost_for_light_regular_package(self):
        """1 кг, 100 км, обычный: 200 + 100*5 = 700."""
        cost, _ = calculate_delivery_cost(1, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_medium_weight_gets_1_2_multiplier(self):
        """10 кг (5 < w < 20): 700 * 1.2 = 840."""
        cost, _ = calculate_delivery_cost(10, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_heavy_weight_gets_1_5_multiplier(self):
        """25 кг (w >= 20): 700 * 1.5 = 1050."""
        cost, _ = calculate_delivery_cost(25, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_weight_exactly_5_has_no_multiplier(self):
        """Вес ровно 5.0 не входит в диапазон (5.0, 20.0) → без множителя → 700."""
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_weight_just_above_5_gets_1_2_multiplier(self):
        """Вес 5.01 входит в диапазон → 700 * 1.2 = 840."""
        cost, _ = calculate_delivery_cost(5.01, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_exactly_20_gets_1_5_multiplier(self):
        """Вес ровно 20.0 попадает в ветку >= 20 → 700 * 1.5 = 1050."""
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_fragile_package_adds_300(self):
        """Хрупкая посылка: 700 + 300 = 1000."""
        cost, _ = calculate_delivery_cost(1, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_dangerous_package_adds_1000(self):
        """Опасная посылка: 700 + 1000 = 1700."""
        cost, _ = calculate_delivery_cost(1, 100, "опасный")
        self.assertEqual(cost, 1700)

    def test_express_makes_delivery_more_expensive(self):
        """Экспресс — платная услуга, стоимость должна быть выше обычной."""
        regular_cost, _ = calculate_delivery_cost(1, 100, "обычный", is_express=False)
        express_cost, _ = calculate_delivery_cost(1, 100, "обычный", is_express=True)
        self.assertGreater(express_cost, regular_cost)

    def test_express_cost_equals_1_5_multiplier(self):
        """Бизнес-логика: экспресс = ×1.5. База 700 → 700 * 1.5 = 1050."""
        cost, _ = calculate_delivery_cost(1, 100, "обычный", is_express=True)
        self.assertEqual(cost, 1050)

    def test_fragile_express_cost(self):
        """Хрупкая + экспресс: (700 + 300) * 1.5 = 1500."""
        cost, _ = calculate_delivery_cost(1, 100, "хрупкий", is_express=True)
        self.assertEqual(cost, 1500)

    def test_dangerous_express_cost(self):
        """Опасная + экспресс: (700 + 1000) * 1.5 = 2550."""
        cost, _ = calculate_delivery_cost(1, 100, "опасный", is_express=True)
        self.assertEqual(cost, 2550)


class TestDeliveryDate(unittest.TestCase):
    """Тесты расчёта даты доставки."""

    def test_distance_1_km_gives_one_day(self):
        """1 км → max(1, 0) = 1 день → 2026-09-04."""
        _, date = calculate_delivery_cost(1, 1, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_short_distance_gives_one_day(self):
        """400 км → 400 // 500 = 0 → max(1, 0) = 1 → 2026-09-04."""
        _, date = calculate_delivery_cost(1, 400, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_500_km_gives_one_day(self):
        """500 км → 500 // 500 = 1 → 2026-09-04."""
        _, date = calculate_delivery_cost(1, 500, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_501_km_gives_one_day(self):
        """501 км → 501 // 500 = 1 (округление вниз) → 2026-09-04."""
        _, date = calculate_delivery_cost(1, 501, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_1000_km_gives_two_days(self):
        """1000 км → 1000 // 500 = 2 → 2026-09-05."""
        _, date = calculate_delivery_cost(1, 1000, "обычный")
        self.assertEqual(date, "2026-09-05")

    def test_1500_km_gives_three_days(self):
        """1500 км → 1500 // 500 = 3 → 2026-09-06."""
        _, date = calculate_delivery_cost(1, 1500, "обычный")
        self.assertEqual(date, "2026-09-06")

    def test_5000_km_gives_ten_days(self):
        """5000 км → 5000 // 500 = 10 → 2026-09-13."""
        _, date = calculate_delivery_cost(1, 5000, "обычный")
        self.assertEqual(date, "2026-09-13")

    def test_express_never_gives_zero_days(self):
        """400 км, экспресс: max(1, 1 // 2) = 1 день → 2026-09-04."""
        _, date = calculate_delivery_cost(1, 400, "обычный", is_express=True)
        self.assertEqual(date, "2026-09-04")


if __name__ == "__main__":
    unittest.main()