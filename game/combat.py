class CombatSystem:
    def __init__(self, game):
        self.game = game
        
    def check_attack_hits(self):
        if self.game.player.is_attacking:
            for enemy in self.game.level.enemies:
                if self.game.player.attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(self.game.player.attack_damage)
                    
    def check_enemy_attacks(self):
        for enemy in self.game.level.enemies:
            if hasattr(enemy, 'is_attacking') and enemy.is_attacking:
                if hasattr(enemy, 'attack_rect') and enemy.attack_rect.colliderect(self.game.player.rect):
                    self.game.player.health_component.take_damage(5)