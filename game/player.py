import pygame
from .asset_loader import asset_loader

class Player:
    class HealthComponent:
        def __init__(self, max_health):
            self.max_health = max_health
            self.current_health = max_health
    
        def take_damage(self, damage):
            """Наносит урон и возвращает True если урон был применен"""
            if self.current_health > 0:
                self.current_health -= damage
                if self.current_health < 0:
                    self.current_health = 0
                return True  # Урон был применен
            return False  # Урон не был применен (уже мертв)
    
        def heal(self, amount):
            """Восстанавливает здоровье"""
            self.current_health += amount
            if self.current_health > self.max_health:
                self.current_health = self.max_health
    
        def is_dead(self):
            """Проверяет, мертв ли игрок"""
            return self.current_health <= 0



    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 60, 135)
        self.hitbox = pygame.Rect(10, 10, 60, 135)
        self.velocity_y = 0
        self.velocity_x = 0
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        self.is_jumping = False
        self.on_ground = False
        self.facing_right = True
        self.show_hitbox = True

        self.coins = 0
        self.keys = 0
        self.jewels = 0
        
        # 🔧 УЛУЧШЕНИЕ: Coyote Time переменные
        self.coyote_time = 0.15
        self.time_since_ground = 0
        self.jump_buffer = 0
        self.jump_buffer_time = 0.1
        
        # 🎨 АНИМАЦИИ
        self.current_state = "idle"
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.animation_timer = 0
        
        # ⚔️ СИСТЕМА УРОНА
        self.is_invincible = False
        self.invincibility_timer = 0
        self.invincibility_duration = 1.0
        self.damage_cooldown = 0.5
        self.last_damage_time = 0
        
        # 🔨 АТАКА ПРЫЖКОМ
        self.bounce_power = -12
        
        # 🎯 ОТСКОК ПРИ УРОНЕ
        self.knockback_power = 8
        self.knockback_duration = 0.3
        self.knockback_timer = 0
        self.is_knockback = False
        
        # 💀 СИСТЕМА СМЕРТИ
        self.is_alive = True
        self.respawn_timer = 0
        self.respawn_duration = 2.0
        self.respawn_position = (x, y)  # 🔥 Сохраняем позицию респавна
        
        self.health_component = self.HealthComponent(60)
        print(f"🎯 Player created at position: ({x}, {y})")
        
        # 🎨 Загрузка всех спрайтов для анимаций
        self.load_sprites()
        self.current_sprite = self.idle_sprite
        
    
    def load_sprites(self):
        """Загружает все спрайты для анимаций"""
        self.idle_sprite = asset_loader.load_image("player/alienPink_front.png",0.7)
        self.run_sprites = [
            asset_loader.load_image("player/alienPink_stand.png", 0.7),
            asset_loader.load_image("player/alienPink_walk1.png", 0.7),
            asset_loader.load_image("player/alienPink_walk2.png", 0.7)
        ]
        self.jump_sprite = asset_loader.load_image("player/alienPink_jump.png",  0.7)
        self.land_sprite = asset_loader.load_image("player/alienPink_duck.png",  0.7)
        
        print("🎨 All player sprites loaded successfully!")
    
    def update_animation(self, moved):
        """Обновляет анимацию в зависимости от состояния игрока"""
        if not self.is_alive:  # 🔥 Не обновляем анимацию если игрок мертв
            return
            
        previous_state = self.current_state
        
        # Определяем текущее состояние
        if not self.on_ground:
            if self.velocity_y < 0:
                self.current_state = "jump"
            else:
                self.current_state = "jump"
        elif moved and not self.is_knockback:
            self.current_state = "run"
        else:
            self.current_state = "idle"
        
        # Если состояние изменилось, сбрасываем анимацию
        if previous_state != self.current_state:
            self.animation_frame = 0
            self.animation_timer = 0
        
        # Обновляем анимацию в зависимости от состояния
        self.animation_timer += self.animation_speed
        
        if self.current_state == "run":
            if self.animation_timer >= 1:
                self.animation_frame = (self.animation_frame + 1) % len(self.run_sprites)
                self.animation_timer = 0
                self.current_sprite = self.run_sprites[self.animation_frame]
        elif self.current_state == "idle":
            self.current_sprite = self.idle_sprite
        elif self.current_state == "jump":
            self.current_sprite = self.jump_sprite
        
        # Анимация приземления
        if previous_state == "jump" and self.current_state == "idle":
            self.current_state = "land"
            self.current_sprite = self.land_sprite
            pygame.time.set_timer(pygame.USEREVENT + 1, 300)
    
    def handle_landing_animation(self):
        """Обрабатывает завершение анимации приземления"""
        self.current_state = "idle"
        self.current_sprite = self.idle_sprite

    def update(self, platforms, enemies, current_time,traps=None):
     
        """Обновление состояния игрока с системой урона"""
        # 💀 ОБНОВЛЕНИЕ РЕСПАВНА
        if not self.is_alive:
            self.respawn_timer -= 1/60
            if self.respawn_timer <= 0:
                self.respawn()
            return  # 🔥 Прерываем обновление если игрок мертв
        if self.rect.y>3000:

            self.health_component.current_health=0
            self.die()
        # 🔪 ПРОВЕРКА СТОЛКНОВЕНИЙ С ШИПАМИ
        if traps and not self.is_invincible and self.is_alive:
            self.check_trap_collisions(traps, current_time)
        
        # ⚔️ Обновляем таймер неуязвимости
        if self.is_invincible:
            self.invincibility_timer -= 1/60
            if self.invincibility_timer <= 0:
                self.is_invincible = False
                print("🛡️ Invincibility ended")
        
        # 🎯 Обновляем таймер отскока
        if self.is_knockback:
            self.knockback_timer -= 1/60
            if self.knockback_timer <= 0:
                self.is_knockback = False
                self.velocity_x = 0
                print("🎯 Knockback ended")
        
        # Сохраняем состояние до обновления
        was_on_ground = self.on_ground
        
        # Применяем гравитацию
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        
        # ПРИМЕНЯЕМ ГОРИЗОНТАЛЬНУЮ СКОРОСТЬ (для отскока)
        if not self.is_knockback:
            if self.jump_buffer > 0:
                self.jump_buffer -= 1/60
        else:
            self.rect.x += self.velocity_x
        
        # Проверка коллизий с платформами
        self.on_ground = False
        for platform in platforms:
            if self.check_collision(platform):
                if self.velocity_y > 0:  # Падение вниз
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.is_jumping = False
                    self.velocity_y = 0
                    self.time_since_ground = 0
                elif self.velocity_y < 0:  # Движение вверх
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
        
        # 🔧 Обновляем Coyote Time
        if self.on_ground:
            self.time_since_ground = 0
        elif was_on_ground:
            self.time_since_ground = 0
        else:
            self.time_since_ground += 1/60
        
        # 🔧 Автопрыжок по буферу (только если нет отскока)
        if not self.is_knockback and self.jump_buffer > 0 and self.can_jump():
            self.jump()
            self.jump_buffer = 0
        
        # ⚔️ Проверка столкновений с врагами
        self.check_enemy_collisions(enemies, current_time)

    def check_enemy_collisions(self, enemies, current_time):
        """Проверяет столкновения с врагами и обрабатывает урон"""
        for enemy in enemies.sprites():
            # 🔥 ПРОВЕРЯЕМ, ЧТО ВРАГ ЖИВ И НЕ В РЕЖИМЕ ПОЛУЧЕНИЯ УРОНА
            if hasattr(enemy, 'is_dead') and enemy.is_dead:
                continue  # Пропускаем мертвых врагов
        
            if hasattr(enemy, 'is_hurt') and enemy.is_hurt:
                continue  # Пропускаем врагов в анимации получения урона
        
            if self.check_collision_with_enemy(enemy):
                # Определяем тип столкновения
                collision_type = self.get_collision_type(enemy)
        
                if collision_type == "top":  # Игрок прыгает на врага сверху
                    # 🔥 ПРОСТО НАНОСИМ УРОН - слайм сам умрет с анимацией
                    self.kill_enemy(enemy)
                    print("🔨 Enemy killed by jump!")
                elif not self.is_invincible and self.is_alive:
                    # Игрок получает урон сбоку или снизу
                    self.take_damage(10, enemy)
                    print("💥 Player took damage from enemy!")

    def get_collision_type(self, enemy):
        """Определяет тип столкновения с врагом"""
        player_bottom = self.rect.bottom
        enemy_top = enemy.rect.top
        player_velocity = self.velocity_y
        
        # Если игрок движется вниз и его низ находится выше середины врага
        if (player_velocity > 0 and 
            player_bottom < enemy.rect.centery and
            self.rect.bottom > enemy.rect.top):
            return "top"
        return "side"

    def kill_enemy(self, enemy):
        """Убивает врага и дает отскок игроку"""
        # 🔥 НАНОСИМ НОРМАЛЬНЫЙ УРОН, а не 100
        enemy.take_damage(30)  # Достаточно чтобы убить слайма с 30 HP
        self.velocity_y = self.bounce_power
        print(f"🎯 Enemy defeated! Bounce: {self.velocity_y}")

    def take_damage(self, damage, enemy):
        """Наносит урон игроку, включает неуязвимость и отскок"""
        if not self.is_invincible and self.is_alive:  # 🔥 ДОБАВЛЕНА ПРОВЕРКА is_alive
            # 🔥 ВАЖНО: Вызываем take_damage у HealthComponent и проверяем результат
            damage_taken = self.health_component.take_damage(damage)
            
            if damage_taken:
                self.is_invincible = True
                self.invincibility_timer = self.invincibility_duration
                self.apply_knockback(enemy)
                
                print(f"❤️ Player health: {self.health_component.current_health}")
                
                # 💀 ПРОВЕРКА СМЕРТИ
                if self.health_component.current_health <= 0:
                    self.die()
                    print("💀 Player died!")

    def apply_knockback(self, enemy):
        """Применяет отскок от врага"""
        # Определяем направление отскока
        if self.rect.centerx < enemy.rect.centerx:
            self.velocity_x = -self.knockback_power
        else:
            self.velocity_x = self.knockback_power
        
        # Небольшой отскок вверх
        self.velocity_y = -self.knockback_power * 0.7
        
        # Включаем режим отскока
        self.is_knockback = True
        self.knockback_timer = self.knockback_duration
        
        print(f"🎯 Knockback applied! Velocity: ({self.velocity_x}, {self.velocity_y})")

    def die(self):
        """Обрабатывает смерть игрока"""
        self.is_alive = False
        self.respawn_timer = self.respawn_duration
        self.velocity_y = 0
        self.velocity_x = 0
        self.is_knockback = False
        self.is_invincible = False
        
        print("💀 Player died! Respawning in 2 seconds...")

    def respawn(self):
        """Возрождает игрока"""
        self.is_alive = True
        self.health_component.current_health = self.health_component.max_health  # 🔥 ВОССТАНАВЛИВАЕМ HP
        self.rect.x = self.respawn_position[0]
        self.rect.y = self.respawn_position[1]
        self.velocity_y = 0
        self.velocity_x = 0
        self.is_invincible = True
        self.invincibility_timer = 3.0  # 🔥 3 секунды неуязвимости после респавна
        self.current_state = "idle"
        self.current_sprite = self.idle_sprite
        
        print("🌟 Player respawned! 3 seconds of invincibility")

    def check_collision_with_enemy(self, enemy):
        """Проверка коллизии с врагом"""
        # 🔥 ПРОВЕРЯЕМ, ЧТО ВРАГ ЖИВ И НЕ В РЕЖИМЕ СМЕРТИ ИЛИ ПОЛУЧЕНИЯ УРОНА
        if hasattr(enemy, 'is_dead') and enemy.is_dead:
            return False  # Мертвые враги не вызывают столкновений
    
        # 🔥 ПРОВЕРЯЕМ, ЧТО ВРАГ НЕ В РЕЖИМЕ ПОЛУЧЕНИЯ УРОНА
        if hasattr(enemy, 'is_hurt') and enemy.is_hurt:
            return False  # Враги в анимации получения урона не вызывают столкновений
    
        player_hitbox = pygame.Rect(
            self.rect.x + self.hitbox.x,
            self.rect.y + self.hitbox.y,
            self.hitbox.width,
            self.hitbox.height
        )
        return player_hitbox.colliderect(enemy.rect)

    def handle_event(self, event):
        """Обработка одиночных событий"""
        if not self.is_alive:  # 🔥 Игнорируем ввод если игрок мертв
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.is_knockback:
                self.jump_buffer = self.jump_buffer_time
                print("💾 Jump input buffered")
        elif event.type == pygame.USEREVENT + 1:
            self.handle_landing_animation()
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)

    def handle_keys(self, keys):
        """Обработка непрерывного ввода клавиш"""
        if not self.is_alive or self.is_knockback:  # 🔥 ДОБАВЛЕНА ПРОВЕРКА is_alive
            return
            
        moved = False
    
        arrow_left = keys[pygame.K_LEFT] 
        arrow_right = keys[pygame.K_RIGHT]
        a_key = keys[pygame.K_a]
        d_key = keys[pygame.K_d]
    
        if arrow_left or a_key:
            self.rect.x -= self.speed
            self.facing_right = False
            moved = True
        if arrow_right or d_key:
            self.rect.x += self.speed
            self.facing_right = True
            moved = True
        
        self.update_animation(moved)

    def can_jump(self):
        return (self.on_ground or 
                self.time_since_ground < self.coyote_time) and not self.is_jumping

    def jump(self):
        if self.can_jump():
            self.velocity_y = self.jump_power
            self.is_jumping = True
            self.on_ground = False
            self.time_since_ground = self.coyote_time

    def check_collision(self, platform):
        """Проверка коллизии с платформой"""
        player_hitbox = pygame.Rect(
            self.rect.x + self.hitbox.x,
            self.rect.y + self.hitbox.y,
            self.hitbox.width,
            self.hitbox.height
        )
        return player_hitbox.colliderect(platform.rect)
    

    def check_trap_collisions(self, traps, current_time):
        """Проверка столкновений с ловушками"""
        for trap in traps:
            if hasattr(trap, 'check_collision') and trap.check_collision(self):
                self.take_damage_from_trap(trap.damage)

    def take_damage_from_trap(self, damage):
        """Получение урона от ловушки"""
        if not self.is_invincible and self.is_alive:
            damage_taken = self.health_component.take_damage(damage)
        
            if damage_taken:
                self.is_invincible = True
                self.invincibility_timer = self.invincibility_duration
            
                # Небольшой отскок от шипов
                self.velocity_y = -8
            
                print(f"🔪 Игрок получил урон от шипов! Здоровье: {self.health_component.current_health}")
            
                if self.health_component.current_health <= 0:
                    self.die()


    def draw(self, screen, camera):
        """Отрисовка игрока с эффектом мигания при неуязвимости"""
        if not self.is_alive:  # 🔥 Не отрисовываем если игрок мертв
            return
            
        screen_x = self.rect.x - camera.offset.x
        screen_y = self.rect.y - camera.offset.y
        
        # ⚔️ Мигание при неуязвимости
        if self.is_invincible and int(self.invincibility_timer * 10) % 2 == 0:
            return
        
        # Отрисовка спрайта
        if self.current_sprite:
            if not self.facing_right:
                flipped_sprite = pygame.transform.flip(self.current_sprite, True, False)
                screen.blit(flipped_sprite, (screen_x, screen_y))
            else:
                screen.blit(self.current_sprite, (screen_x, screen_y))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (screen_x, screen_y, 40, 60))
        
        # Отрисовка хитбокса (для отладки)
        if self.show_hitbox:
            hitbox_rect = pygame.Rect(
                screen_x + self.hitbox.x,
                screen_y + self.hitbox.y,
                self.hitbox.width,
                self.hitbox.height
            )
            pygame.draw.rect(screen, (255, 0, 0), hitbox_rect, 2)

    