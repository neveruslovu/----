"""
Система боя и взаимодействий
"""

class CombatSystem:
    def __init__(self, game):
        self.game = game
        
    def check_attack_hits(self):
        """Проверка попаданий атаки игрока"""
        if self.game.player.is_attacking:
            for enemy in self.game.level.enemies:
                if self.game.player.attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(self.game.player.attack_damage)
    
    def check_enemy_attacks(self):
        """Проверка атак врагов по игроку"""
        for enemy in self.game.level.enemies:
            if hasattr(enemy, 'is_attacking') and enemy.is_attacking:
                if hasattr(enemy, 'attack_rect') and enemy.attack_rect.colliderect(self.game.player.rect):
                    # Урон наносится внутри класса врага
                    pass
    
    def update(self, dt):
        """Обновление боевой системы"""
        self.check_attack_hits()
        self.check_enemy_attacks()