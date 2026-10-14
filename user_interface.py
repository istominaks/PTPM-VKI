from abc import ABC, abstractmethod


class UserInterface(ABC):
    """Абстрактный базовый класс взаимодействия с пользователем."""

    @abstractmethod
    def get_input(self):
        """Получить входные данные от пользователя."""
        pass


class ConsoleUserInterface(UserInterface):
    """Реализация взаимодействия с пользователем через консоль."""

    def get_input(self):
        side_a = input("Введите сторону A: ")
        side_b = input("Введите сторону B: ")
        side_c = input("Введите сторону C: ")
        return side_a, side_b, side_c