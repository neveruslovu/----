class HealthComponent:
    def __init__(self, max_health):
        self.max_health = max_health
        self.current_health = max_health
        self.invulnerable = False
        self.invulnerability_timer = 0
        
    def take_damage(self, amount):
        if not self.invulnerable and self.current_health > 0:
            self.current_health = max(0, self.current_health - amount)
            self.invulnerable = True
            self.invulnerability_timer = 0.5
            return True
        return False
    
    def heal(self, amount):
        self.current_health = min(self.max_health, self.current_health + amount)
    
    def update(self, dt):
        if self.invulnerable:
            self.invulnerability_timer -= dt
            if self.invulnerability_timer <= 0:
                self.invulnerable = False
    
    def is_dead(self):
        return self.current_health <= 0