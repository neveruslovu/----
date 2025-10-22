"""
Загрузчик спрайтов для игры
"""

import pygame
import os

class AssetLoader:
    def __init__(self):
        self.assets = {}
        self.base_path = "assets"
        
    def load_image(self, path, scale=1, alpha=True):
        """Загрузка изображения с обработкой ошибок"""
        try:
            full_path = os.path.join(self.base_path, path)
            if alpha:
                image = pygame.image.load(full_path).convert_alpha()
            else:
                image = pygame.image.load(full_path).convert()
            
            if scale != 1:
                new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
                image = pygame.transform.scale(image, new_size)
                
            return image
        except pygame.error as e:
            print(f"❌ Не удалось загрузить спрайт: {full_path}")
            print(f"Ошибка: {e}")
            # Создаем цветную заглушку
            surf = pygame.Surface((32, 32))
            surf.fill((255, 0, 255))  # Фиолетовый для заметности
            return surf
    
    def load_spritesheet_frames(self, path, columns, scale=1):
        """Загрузка кадров из спрайт-листа"""
        try:
            sprite_sheet = self.load_image(path, scale, alpha=True)
            if not sprite_sheet:
                return []
            
            sheet_width = sprite_sheet.get_width()
            frame_width = sheet_width // columns
            
            frames = []
            for i in range(columns):
                frame = sprite_sheet.subsurface(pygame.Rect(
                    i * frame_width, 0,
                    frame_width, sprite_sheet.get_height()
                ))
                frames.append(frame)
            
            return frames
            
        except Exception as e:
            print(f"❌ Ошибка загрузки спрайт-листа {path}: {e}")
            return []

# Глобальный загрузчик
asset_loader = AssetLoader()