from abc import ABC, abstractmethod
import logging


class Notifier(ABC):
    """Абстрактный базовый класс сторонней зависимости."""

    @abstractmethod
    def send(self, message):
        """Имитация отправки данных стороннему процессу."""
        pass


class EmailNotifier(Notifier):
    """Имитация отправки данных на email-сервер."""

    def send(self, message):
        logging.info(f"[ИМИТАЦИЯ EMAIL] Отправлено сообщение: {message}")
        return True