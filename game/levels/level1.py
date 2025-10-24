# game/levels/level1.py
import pygame
import base64
import zlib
import os
from ..platform import Platform
from ..enemies.slime import Slime
from ..asset_loader import asset_loader

class Level:
    def __init__(self, name):
        print(f"🗺️ Creating level: {name}")
        self.name = name
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.background = asset_loader.load_image("backgrounds/colored_grass.png", 1)
        
        self.player = None
        self.player_spawn_point = (256, 1576)  # 🔥 ПО УМОЛЧАНИЮ - позиция из вашего XML
        self.width = 30 * 128
        self.height = 20 * 128
        
        # Загружаем уровень из XML
        self.load_from_xml()
        print(f"🗺️ Уровень '{name}' создан! Спавн игрока: {self.player_spawn_point}")
    
    def set_player(self, player):
        """Установить ссылку на игрока"""
        self.player = player
        # 🔥 УСТАНАВЛИВАЕМ ПОЗИЦИЮ ИГРОКА ИЗ УРОВНЯ
        if self.player:
            self.player.rect.x = self.player_spawn_point[0]
            self.player.rect.y = self.player_spawn_point[1]
            self.player.respawn_position = self.player_spawn_point
    
    def decode_layer_data(self):
        """Декодирование данных слоя тайлов из base64+zlib"""
        encoded_data = "eJxjYBhegAUJk6pnsANquZOTCmaQahYLA3lxg88cagBhKplDLKC2+6kFaOkuVhqYiQzoGabsVDaP2LBhIyAvhMTmgJqLnDdFkOwDiXMRaS96vqUFJgUQE/7cUExNgC38aZGuOZEwKxJGFgfFHTnlliADbjcPtngeLgAAwS0CVQ=="
        decoded = base64.b64decode(encoded_data)
        decompressed = zlib.decompress(decoded)
        
        # Конвертируем в список тайлов
        tile_data = []
        for i in range(0, len(decompressed), 4):
            tile_gid = int.from_bytes(decompressed[i:i+4], byteorder='little')
            tile_data.append(tile_gid)
        
        return tile_data
    
    def load_from_xml(self):
        """Загрузка уровня из XML данных"""
        try:
            # Декодируем тайловую карту
            tile_data = self.decode_layer_data()
            
            # Соответствие GID типам платформ
            gid_to_type = {
                1: "grass_half_left",
                2: "grass_half_mid", 
                3: "grass_half_right",
                4: "grass_half",
                5: "grass",
                6: "door_mid",
                7: "door_top",
                8: "grass_hill_right", 
                9: "spikes",
                10: "grass_round",
                11: "box",
                12: "lock_yellow",
                13: "coin",
                14: "key_yellow", 
                15: "jewel_blue",
                16: "fly",
                17: "saw",
                18: "slime",
                19: "mushroom",
                20: "snail",
                21: "player_spawn"  # 🔥 ТОЧКА СПАВНА ИГРОКА
            }
            
            # Создаем платформы из тайловой карты
            for y in range(20):
                for x in range(30):
                    tile_index = y * 30 + x
                    tile_gid = tile_data[tile_index]
                    
                    if tile_gid in gid_to_type:
                        platform_type = gid_to_type[tile_gid]
                        
                        # 🔥 ОСОБАЯ ОБРАБОТКА ДЛЯ ТОЧКИ СПАВНА ИГРОКА
                        if tile_gid == 21:
                            self.player_spawn_point = (x * 128, y * 128)
                            continue  # Не создаем платформу для точки спавна
                        
                        is_trap = (tile_gid == 9)
                        is_door = (tile_gid in [6, 7])
                        
                        platform = Platform(
                            x * 128, y * 128, 128, 128,
                            platform_type=platform_type,
                            is_trap=is_trap,
                            is_door=is_door
                        )
                        
                        if is_trap:
                            self.traps.add(platform)
                        elif is_door:
                            self.doors.add(platform)
                        else:
                            self.platforms.add(platform)
            
            # 🔥 ДОБАВЛЯЕМ ОБЪЕКТЫ ИЗ OBJECTGROUP
            self.add_objects_from_xml()
            
            # Добавляем врагов
            self.add_enemies()
            
        except Exception as e:
            print(f"❌ Ошибка загрузки уровня: {e}")
            self.create_fallback_level()
    
    def add_objects_from_xml(self):
        """Добавляем объекты из objectgroup XML"""
        # Объекты из objectgroup id="2"
        objects_data = [
            # (x, y, width, height, type, gid)
            (1094.67, 1976.33, 32, 32, "lock_yellow", 12),      # Желтый замок
            (640, 1280, 128, 128, "coin", 13),                  # Монеты
            (768, 1280, 128, 128, "coin", 13),
            (896, 1280, 128, 128, "coin", 13),
            (2236, 368, 128, 128, "coin", 13),
            (2420, 1008, 128, 128, "coin", 13),
            (696, 236, 128, 128, "key_yellow", 14),             # Желтый ключ
            (2944, 116, 128, 128, "jewel_blue", 15),            # Синий джевел
            (3100, 1596, 128, 128, "coin", 13),
            (3584, 2012, 128, 128, "coin", 13),
            (2884, 2000, 128, 128, "fly", 16),                  # Муха (враг)
        ]
        
        for x, y, w, h, obj_type, gid in objects_data:
            platform = Platform(x, y, w, h, platform_type=obj_type)
            
            if gid == 16:  # Враг fly
                # Временно как платформа, позже заменить на класс Fly
                self.platforms.add(platform)
            else:
                self.platforms.add(platform)
    
    def add_enemies(self):
        """Добавляем врагов на уровень"""
        # Слаймы на земле
        self.enemies.add(Slime(500, 2272))  # На основной земле
        self.enemies.add(Slime(800, 2272))
        self.enemies.add(Slime(1200, 2272))
        
        # Слаймы на платформах
        self.enemies.add(Slime(150, 268))   # На платформе (300 - 32)
        self.enemies.add(Slime(350, 468))   # На платформе (500 - 32)
    
    def create_fallback_level(self):
        """Резервный уровень если XML не загрузился"""
        print("🔄 Создаю резервный уровень...")
        
        # Основная земля
        for x in range(0, 3840, 128):
            self.platforms.add(Platform(x, 2400, 128, 128, "grass"))
        
        # Несколько платформ
        platforms_data = [
            (100, 300, 100, 20),
            (300, 500, 100, 20),
            (500, 600, 100, 20),
        ]
        
        for x, y, w, h in platforms_data:
            self.platforms.add(Platform(x, y, w, h, "grass"))
        
        self.add_enemies()
    
    def update(self, dt):
        """Обновление уровня"""
        for enemy in self.enemies:
            enemy.update(dt, self)
    
    def draw(self, screen, camera):
        """Отрисовка уровня"""
        screen.blit(self.background, (0, 0))
        
        for platform in self.platforms:
            platform.draw(screen, camera)
        
        for door in self.doors:
            door.draw(screen, camera)
        
        for trap in self.traps:
            trap.draw(screen, camera)
        
        for enemy in self.enemies:
            enemy.draw(screen, camera)