# game/__init__.py
# Оставляем только базовые импорты, без циклических зависимостей
from .player import Player
from .platform import Platform
from .camera import Camera

__all__ = ['Player', 'Platform', 'Camera']