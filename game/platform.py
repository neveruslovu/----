import pygame
from .asset_loader import asset_loader

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, platform_type="grass", is_trap=False, is_door=False):
        super().__init__()
        
        self.platform_type = platform_type
        self.is_trap = is_trap
        self.is_door = is_door
        
        # Словарь с путями к спрайтам для разных типов платформ
        sprite_paths = {
            #platforms
            "grass": "ground/Grass/grass.png",
            "grass_half": "ground/Grass/grassHalf.png",
            "grass_half_left": "ground/Grass/grassHalf_left.png",
            "grass_half_mid": "ground/Grass/grassHalf_mid.png",
            "grass_half_right": "ground/Grass/grassHalf_right.png",
            "grass_hill_right": "ground/Grass/grassHill_right.png",
            "grass_round": "ground/Grass/grassCenter_round.png",

            "box": "tiles/boxItem.png",

            "spikes": "tiles/spikes.png",

            "mushroom": "tiles/mushroomRed.png",

            "door_top": "tiles/doorClosed_top.png",
            "door_mid": "tiles/doorClosed_mid.png",
            "doorOpen_mid": "tiles/doorOpen_mid.png",
            "doorOpen_top": "tiles/doorOpen_top.png",

            "signExit": "tiles/signExit.png",

            "bush": "tiles/bush.png",
            "cactus": "tlies/cactus.png"


        }
        
        # Цвета для заглушек по типам
        fallback_colors = {
            "grass": (100, 200, 100),        # Зеленый
            "grass_half": (120, 220, 120),   # Светло-зеленый
            "grass_half_left": (80, 180, 80),
            "grass_half_mid": (90, 190, 90),
            "grass_half_right": (80, 180, 80),
            "grass_hill_right": (110, 210, 110),
            "grass_round": (130, 230, 130),
            "box": (150, 100, 50),           # Коричневый
            "spikes": (255, 50, 50),         # Красный
            "door_mid": (200, 150, 50),      # Золотистый
            "door_top": (180, 130, 30),
            "mushroom": (255, 100, 100)      # Красный для гриба
        }
        
        self.image = None
        sprite_path = sprite_paths.get(platform_type, "grass")
        
        try:
            self.image = asset_loader.load_image(sprite_path, scale=1)
            self.image = pygame.transform.scale(self.image, (width, height))
            print(f"✅ Загружен спрайт: {sprite_path}")
        except Exception as e:
            # Создаем цветную заглушку
            self.image = pygame.Surface((width, height))
            color = fallback_colors.get(platform_type, (100, 100, 100))
            self.image.fill(color)
            
            # Добавляем узоры для разных типов
            if platform_type == "spikes" or is_trap:
                # Рисуем шипы
                spike_height = height // 2
                for i in range(0, width, width // 4):
                    points = [
                        (i, height),
                        (i + width // 8, height - spike_height),
                        (i + width // 4, height)
                    ]
                    pygame.draw.polygon(self.image, (200, 30, 30), points)
            
            elif platform_type.startswith("door") or is_door:
                # Рисуем дверь с ручкой
                pygame.draw.rect(self.image, (100, 70, 20), 
                               (width // 4, height // 4, width // 2, height // 2))
                pygame.draw.circle(self.image, (50, 50, 50), 
                                 (width * 3 // 4, height // 2), width // 10)
            
            elif platform_type == "box":
                # Рисуем текстуру ящика
                pygame.draw.rect(self.image, (120, 80, 40), 
                               (0, 0, width, height))
                pygame.draw.rect(self.image, (100, 60, 30), 
                               (width // 4, height // 4, width // 2, height // 2))
            
            print(f"🔄 Использую заглушку для: {platform_type}")
        
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))