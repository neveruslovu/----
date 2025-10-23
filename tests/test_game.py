import unittest
import sys
import os
import pygame

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from game.game import Game

class TestGame(unittest.TestCase):
    """Тесты для основного класса Game"""
    
    def setUp(self):
        pygame.init()
        self.screen = pygame.Surface((800, 600))
        self.game = Game(self.screen)
    
    def tearDown(self):
        pygame.quit()
    
    def test_game_initialization(self):
        """Тест инициализации игры"""
        self.assertIsNotNone(self.game.player)
        self.assertIsNotNone(self.game.camera)
        self.assertIsNotNone(self.game.level)
        self.assertGreater(len(self.game.level), 0)
    
    def test_game_update(self):
        """Тест обновления игры"""
        # Должно выполняться без ошибок
        try:
            self.game.update(0.016)  # 60 FPS
            success = True
        except Exception as e:
            success = False
            print(f"Ошибка обновления: {e}")
        
        self.assertTrue(success)
    
    def test_game_draw(self):
        """Тест отрисовки игры"""
        # Должно выполняться без ошибок
        try:
            self.game.draw(self.screen)
            success = True
        except Exception as e:
            success = False
            print(f"Ошибка отрисовки: {e}")
        
        self.assertTrue(success)
    
    def test_game_event_handling(self):
        """Тест обработки событий"""
        # Создаем mock событие прыжка
        jump_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
        events = [jump_event]
        
        # Должно выполняться без ошибок
        try:
            self.game.handle_events(events)
            success = True
        except Exception as e:
            success = False
            print(f"Ошибка обработки событий: {e}")
        
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()