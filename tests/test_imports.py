import unittest
import sys
import os

class TestImports(unittest.TestCase):
    def test_import_modules(self):
        """Тест импорта всех модулей"""
        modules_to_test = [
            'game.player',
            'game.platform', 
            'game.camera',
            'game.game',
            'game.assets'
        ]
        
        for module_name in modules_to_test:
            try:
                __import__(module_name)
                success = True
            except ImportError as e:
                success = False
                print(f"Import error in {module_name}: {e}")
            self.assertTrue(success, f"Failed to import {module_name}")

if __name__ == '__main__':
    unittest.main()