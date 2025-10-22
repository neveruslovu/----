"""
Система анимаций для спрайтов
"""

import pygame

class Animation:
    def __init__(self, frames, frame_duration=0.1, loop=True):
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.timer = 0
        self.done = False
        
    def update(self, dt):
        """Обновление анимации"""
        if self.done:
            return
            
        self.timer += dt
        if self.timer >= self.frame_duration:
            self.timer = 0
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.done = True
    
    def get_current_frame(self):
        """Получить текущий кадр"""
        return self.frames[self.current_frame]
    
    def reset(self):
        """Сбросить анимацию"""
        self.current_frame = 0
        self.timer = 0
        self.done = False

class SpriteSheet:
    """Для загрузки спрайтов из sprite sheet"""
    def __init__(self, filename, frame_width, frame_height):
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frames = []
        
        self.load_frames()
    
    def load_frames(self):
        """Загрузка всех кадров из sprite sheet"""
        sheet_width, sheet_height = self.sheet.get_size()
        
        for y in range(0, sheet_height, self.frame_height):
            for x in range(0, sheet_width, self.frame_width):
                frame = self.sheet.subsurface(
                    pygame.Rect(x, y, self.frame_width, self.frame_height)
                )
                self.frames.append(frame)
    
    def get_frames(self, start, count):
        """Получить диапазон кадров"""
        return self.frames[start:start + count]