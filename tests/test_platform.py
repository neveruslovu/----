import unittest
import sys
import os
import pygame

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from game.platform import Platform

class TestPlatform(unittest.TestCase):
    """Тесты для класса Platform"""
    
    def setUp(self):
        pygame.init()
    
    def tearDown(self):
        pygame.quit()
    
    def test_platform_creation(self):
        """Тест создания платформы"""
        platform = Platform(100, 200, 300, 50)
        
        self.assertEqual(platform.rect.x, 100)
        self.assertEqual(platform.rect.y, 200)
        self.assertEqual(platform.rect.width, 300)
        self.assertEqual(platform.rect.height, 50)
    
    def test_platform_draw(self):
        """Тест отрисовки платформы"""
        platform = Platform(100, 200, 300, 50)
        screen = pygame.Surface((800, 600))
        
        # Mock camera
        class MockCamera:
            x = 0
            y = 0
        
        camera = MockCamera()
        
        # Должно выполняться без ошибок
        try:
            platform.draw(screen, camera)
            success = True
        except Exception as e:
            success = False
            print(f"Ошибка отрисовки: {e}")
        
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()