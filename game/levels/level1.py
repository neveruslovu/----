# game/levels/level1.py
import pygame
import base64
import zlib
import os
from ..platform import Platform
from ..enemies.slime import Slime
from ..enemies.snail import Snail
from ..enemies.fly import Fly
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
        self.player_spawn_point = (256, 700)  # 🔥 ПО УМОЛЧАНИЮ
        self.width = 30 * 128
        self.height = 20 * 128
        
        # Загружаем уровень из XML
        self.load_from_xml()
        print(f"🗺️ Уровень '{name}' создан! Спавн игрока: {self.player_spawn_point}")
    
    def set_player(self, player):
        """Установить ссылку на игрока"""
        self.player = player
        if self.player:
            self.player.rect.x = self.player_spawn_point[0]
            self.player.rect.y = self.player_spawn_point[1]
            self.player.respawn_position = self.player_spawn_point
    
    def decode_layer_data(self, encoded_data):
        """Декодирование данных слоя тайлов из base64+zlib"""
        try:
            # Убираем пробелы и переносы строк
            encoded_data = encoded_data.strip().replace('\n', '').replace('\r', '')
            
            decoded = base64.b64decode(encoded_data)
            decompressed = zlib.decompress(decoded)
            
            # Конвертируем в список тайлов
            tile_data = []
            for i in range(0, len(decompressed), 4):
                tile_gid = int.from_bytes(decompressed[i:i+4], byteorder='little')
                tile_data.append(tile_gid)
            
            return tile_data
        except Exception as e:
            print(f"❌ Ошибка декодирования слоя: {e}")
            return []
    
    def load_from_xml(self):
        """Загрузка уровня из XML данных"""
        try:
            # 🔥 ОСНОВНОЙ СЛОЙ ТАЙЛОВ (layer id="4")
            main_layer_data = "eJxjYBi5gAWKqQlY0fBwBKT6jYWBNmFNCRAmUx85ccvCMDjDABug1H+0BlJ0sAOb3yWhtDgUg4AYkjyMLYxDPzH2ceGQoycejIB9gOxlA2IJGpqPLbyxxQWITW55hQ1wMdA3TQ329EVLAACnnwK2"
            tile_data = self.decode_layer_data(main_layer_data)
            
            # 🔥 РАСШИРЕННОЕ СООТВЕТСТВИЕ GID ТИПАМ ПЛАТФОРМ
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
                21: "player_spawn",
                22: "cactus",
                23: "bush",
                24: "sign_exit",
                25: "door_open_mid",
                26: "door_open_top"
            }
            
            # Создаем платформы из тайловой карты
            for y in range(20):
                for x in range(30):
                    tile_index = y * 30 + x
                    if tile_index < len(tile_data):
                        tile_gid = tile_data[tile_index]
                        
                        if tile_gid in gid_to_type:
                            platform_type = gid_to_type[tile_gid]
                            
                            # 🔥 ОСОБАЯ ОБРАБОТКА ДЛЯ ТОЧКИ СПАВНА ИГРОКА
                            if tile_gid == 21:
                                self.player_spawn_point = (x * 128, y * 128)
                                continue  # Не создаем платформу для точки спавна
                            
                            is_trap = (tile_gid == 9)
                            is_door = (tile_gid in [6, 7, 25, 26])
                            
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
            
            # 🔥 ОБНОВЛЕННЫЕ ОБЪЕКТЫ ИЗ OBJECTGROUP
            self.add_objects_from_xml()
            
            # Добавляем врагов из объектов
            self.add_enemies_from_objects()
            
        except Exception as e:
            print(f"❌ Ошибка загрузки уровня: {e}")
            self.create_fallback_level()
    
    def add_objects_from_xml(self):
        """Добавляем объекты из objectgroup XML"""
        # 🔥 ОБНОВЛЕННЫЕ ОБЪЕКТЫ ИЗ ВАШЕГО НОВОГО XML
        objects_data = [
            # Ключи и предметы
            (442, 256, 128, 128, "key_yellow", 14),             # Желтый ключ
            (710.667, 1977.33, 32, 32, "lock_yellow", 12),      # Желтый замок
            (3200, 256, 128, 128, "jewel_blue", 15),            # Синий джевел
            
            # Монеты
            (384, 1152, 128, 128, "coin", 13),
            (640, 1152, 128, 128, "coin", 13),
            (896, 896, 128, 128, "coin", 13),
            (1024, 896, 128, 128, "coin", 13),
            (1152, 896, 128, 128, "coin", 13),
            (640, 640, 128, 128, "coin", 13),
            (2688, 1024, 128, 128, "coin", 13),
            (2688, 512, 128, 128, "coin", 13),
            (2816, 512, 128, 128, "coin", 13),
            (3072, 768, 128, 128, "coin", 13),
            
            # Ящики
            (2048, 1920, 128, 128, "box", 11),
            (2176, 1920, 128, 128, "box", 11),
        ]
        
        for x, y, w, h, obj_type, gid in objects_data:
            platform = Platform(x, y, w, h, platform_type=obj_type)
            self.platforms.add(platform)
    
    def add_enemies_from_objects(self):
        """Добавляем врагов из объектов XML"""
        # 🔥 ВРАГИ ИЗ OBJECTGROUP
        enemies_data = [
            # Мухи (gid=16)
            (2688, 1920, 128, 128, "fly", 16),
            (2688, 2048, 128, 128, "fly", 16),
            
            # Пила (gid=17)
            (3584, 2176, 128, 128, "saw", 17),
            
            # Слаймы (gid=18)
            (896, 1536, 128, 128, "slime", 18),
            (512, 1536, 128, 128, "slime", 18),
            (1152, 1536, 128, 128, "slime", 18),
            
            # Улитки (gid=20)
            (2176, 1536, 128, 128, "snail", 20),
            (2560, 1536, 128, 128, "snail", 20),
        ]
        
        for x, y, w, h, enemy_type, gid in enemies_data:
            if enemy_type == "slime":
                self.enemies.add(Slime(x, y))
            elif enemy_type == "snail":
                # 🔥 ДОБАВЬТЕ КЛАСС Snail ЕСЛИ ЕГО ЕЩЕ НЕТ
                try:
                    self.enemies.add(Snail(x, y))
                except:
                    # Временно используем Slime вместо Snail
                    self.enemies.add(Slime(x, y))
            else:
                # Для fly и saw временно создаем платформы
                platform = Platform(x, y, w, h, platform_type=enemy_type)
                self.platforms.add(platform)
        
        # 🔥 ДОБАВЛЯЕМ ШИПЫ КАК ЛОВУШКИ
        spikes_data = [
            (896, 2176, 128, 128), (1024, 2176, 128, 128),
            (0, 2176, 128, 128), (128, 2176, 128, 128),
            (256, 2176, 128, 128), (384, 2176, 128, 128),
            (1536, 1536, 128, 128), (1664, 1536, 128, 128),
            (1792, 1536, 128, 128), (3072, 1536, 128, 128),
            (3328, 768, 128, 128), (384, 640, 128, 128),
            (512, 640, 128, 128), (512, 1152, 128, 128),
            (2944, 2176, 128, 128), (3072, 2176, 128, 128),
            (3200, 2176, 128, 128)
        ]
        
        for x, y, w, h in spikes_data:
            spike = Platform(x, y, w, h, platform_type="spikes", is_trap=True)
            self.traps.add(spike)
    
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
        
        # Базовые враги
        self.enemies.add(Slime(500, 2272))
        self.enemies.add(Slime(800, 2272))
    
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