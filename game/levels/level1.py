# game/levels/level1.py
import pygame
import base64
import zlib
import os
from ..platform import Platform
from ..enemies.slime import Slime
from ..enemies.snail import Snail
from ..enemies.fly import Fly
from ..items.items import Item
from ..decorations import Decoration
from ..asset_loader import asset_loader
from ..enemies.saw import Saw
from ..traps.spikes import Spikes
class Level:
    def __init__(self, name):
        print(f"🗺️ Creating level: {name}")
        self.name = name
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.decorations = pygame.sprite.Group()
        self.background = asset_loader.load_image("backgrounds/colored_grass.png", 1)
        
        self.player = None
        self.player_spawn_point = (256, 700)
        self.width = 30 * 128
        self.height = 20 * 128
        
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
                1: "grass_half_left", 2: "grass_half_mid", 3: "grass_half_right",
                4: "grass_half", 5: "grass", 6: "door_mid", 7: "door_top",
                8: "grass_hill_right", 9: "spikes", 10: "grass_round",
                11: "box", 12: "lock_yellow", 13: "coin", 14: "key_yellow", 
                15: "jewel_blue", 16: "fly", 17: "saw", 18: "slime",
                19: "mushroom", 20: "snail", 21: "player_spawn",
                22: "cactus", 23: "bush", 24: "signExit",
                25: "doorOpen_mid", 26: "doorOpen_top"
            }
            
            # Создаем платформы из тайловой карты
            for y in range(20):
                for x in range(30):
                    tile_index = y * 30 + x
                    if tile_index < len(tile_data):
                        tile_gid = tile_data[tile_index]
                        
                        if tile_gid in gid_to_type:
                            platform_type = gid_to_type[tile_gid]
                            
                            if tile_gid == 21:  # Точка спавна
                                self.player_spawn_point = (x * 128, y * 128)
                                continue
                            
                            # 🔥 РАЗДЕЛЕНИЕ ОБЪЕКТОВ ПО ТИПАМ
                            if tile_gid in [19, 22, 23, 24]:  # Фоновые объекты
                                decoration = Decoration(x * 128, y * 128, 128, 128, platform_type)
                                self.decorations.add(decoration)
                                
                            elif tile_gid == 9:  # Шипы
                                # 🔥 ПОДНИМАЕМ ШИПЫ НА РАЗМЕР ТАЙЛА ВВЕРХ
                                platform = Platform(x * 128, y * 128 - 128, 128, 128, platform_type, is_trap=True)
                                self.traps.add(platform)
                                
                            elif tile_gid in [6, 7, 25, 26]:  # Двери
                                platform = Platform(x * 128, y * 128, 128, 128, platform_type, is_door=True)
                                self.doors.add(platform)
                                
                            else:  # Обычные платформы
                                platform = Platform(x * 128, y * 128, 128, 128, platform_type)
                                self.platforms.add(platform)
            
            # 🔥 ОБНОВЛЕННЫЕ МЕТОДЫ ДЛЯ ОБЪЕКТОВ
            self.add_items_from_xml()
            self.add_enemies_from_objects()
            self.add_decorations_from_xml()
            
        except Exception as e:
            print(f"❌ Ошибка загрузки уровня: {e}")
            self.create_fallback_level()
    
    def add_items_from_xml(self):
        """Добавляем собираемые предметы"""
        items_data = [
            (442, 256, 128, 128, "key_yellow"),
            (3200, 256, 128, 128, "jewel_blue"),
            
            # Монеты
            (384, 1152, 128, 128, "coin"),
            (640, 1152, 128, 128, "coin"),
            (896, 896, 128, 128, "coin"),
            (1024, 896, 128, 128, "coin"),
            (1152, 896, 128, 128, "coin"),
            (640, 640, 128, 128, "coin"),
            (2688, 1024, 128, 128, "coin"),
            (2688, 512, 128, 128, "coin"),
            (2816, 512, 128, 128, "coin"),
            (3072, 768, 128, 128, "coin"),
        ]
        
        for x, y, w, h, item_type in items_data:
            item = Item(x, y, w, h, item_type)
            self.items.add(item)
    
    def add_decorations_from_xml(self):
        """Добавляем фоновые объекты (не взаимодействуют с игроком)"""
        decorations_data = [
            # Ящики (не собираемые)
            (2048, 1920, 128, 128, "box"),
            (2176, 1920, 128, 128, "box"),
            # Замок (не собираемый)
            (710.667, 1977.33, 32, 32, "lock_yellow"),
        ]
        
        for x, y, w, h, deco_type in decorations_data:
            decoration = Decoration(x, y, w, h, deco_type)
            self.decorations.add(decoration)
    
    def add_enemies_from_objects(self):
        """Добавляем врагов из объектов XML"""
        enemies_data = [
            # Мухи
            (2688, 1920, 128, 128, "fly"),
            (2688, 2048, 128, 128, "fly"),
            
            # Пила
            (3584, 2176, 128, 128, "saw"),
            
            # Слаймы
            (896, 1536, 128, 128, "slime"),
            (512, 1536, 128, 128, "slime"),
            (1152, 1536, 128, 128, "slime"),
            
            # Улитки
            (2176, 1536, 128, 128, "snail"),
            (2560, 1536, 128, 128, "snail"),
            
        ]
        
        for x, y, w, h, enemy_type in enemies_data:
            try:
                if enemy_type == "slime":
                    enemy = Slime(x, y)
                elif enemy_type == "snail":
                    enemy = Snail(x, y)
                elif enemy_type == "fly":
                    enemy = Fly(x, y)
                elif enemy_type == "saw":
                    enemy = Saw(x, y)
            
                self.enemies.add(enemy)
                print(f"✅ Враг {enemy_type} создан на позиции ({x}, {y})")
            
            except Exception as e:
                print(f"❌ Ошибка создания врага {enemy_type}: {e}")
                # Создаем слайма как запасной вариант
                fallback_enemy = Slime(x, y)
                self.enemies.add(fallback_enemy)
                print(f"🔄 Создан слайм вместо {enemy_type}")
        
        # 🔥 ШИПЫ КАК ЛОВУШКИ - ПОДНИМАЕМ НА РАЗМЕР ТАЙЛА
        spikes_data = [
            (896, 2176 - 128, 128, 128), (1024, 2176 - 128, 128, 128),
            (0, 2176 - 128, 128, 128), (128, 2176 - 128, 128, 128),
            (256, 2176 - 128, 128, 128), (384, 2176 - 128, 128, 128),
            (1536, 1536 - 128, 128, 128), (1664, 1536 - 128, 128, 128),
            (1792, 1536 - 128, 128, 128), (3072, 1536 - 128, 128, 128),
            (3328, 768 - 128, 128, 128), (384, 640 - 128, 128, 128),
            (512, 640 - 128, 128, 128), (512, 1152 - 128, 128, 128),
            (2944, 2176 - 128, 128, 128), (3072, 2176 - 128, 128, 128),
            (3200, 2176 - 128, 128, 128)
        ]
        
        for x, y, w, h in spikes_data:
            spike = Spikes(x, y, w, h)  # ✅ Используем класс Spikes
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
        
        print("✅ Резервный уровень создан")
    
    def update(self, dt):
        """Обновление уровня"""
        for enemy in self.enemies:
            enemy.update(dt, self)
        
        # 🔥 ПРОВЕРКА СБОРА ПРЕДМЕТОВ
        if self.player:
            self.check_item_collection()
    
    def check_item_collection(self):
        """Проверка сбора предметов игроком"""
        for item in self.items.sprites():
            if not item.collected and self.player.rect.colliderect(item.rect):
                item_type = item.collect()
                if item_type:
                    print(f"🎁 Собран предмет: {item_type}")
                    # 🔥 ОБНОВЛЯЕМ СЧЕТЧИКИ ИГРОКА
                    if item_type == "coin":
                        self.player.coins += 1
                    elif item_type == "key_yellow":
                        self.player.keys += 1
                    elif item_type == "jewel_blue":
                        self.player.jewels += 1
    
    def draw(self, screen, camera):
        """Отрисовка уровня в правильном порядке"""
        screen.blit(self.background, (0, 0))
        
        # 🔥 ПРАВИЛЬНЫЙ ПОРЯДОК ОТРИСОВКИ:
        
        # 1. Основные платформы и земля
        for platform in self.platforms:
            platform.draw(screen, camera)
        
        # 2. Декорации (рисуются ПОД врагами и предметами)
        for decoration in self.decorations:
            decoration.draw(screen, camera)
        
        # 3. Шипы (рисуются ПОВЕРХ платформ)
        for trap in self.traps:
            trap.draw(screen, camera)
        
        # 4. Двери
        for door in self.doors:
            door.draw(screen, camera)
        
        # 5. Враги
        for enemy in self.enemies:
            enemy.draw(screen, camera)
        
        # 6. Предметы (рисуются ПОВЕРХ всего)
        for item in self.items:
            item.draw(screen, camera)