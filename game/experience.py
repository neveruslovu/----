class ExperienceSystem:
    def __init__(self, player):
        self.player = player
        self.current_exp = 0
        self.current_level = 1
        self.exp_to_next_level = 100
        self.skill_points = 0
        
    def add_exp(self, amount):
        self.current_exp += amount
        while self.current_exp >= self.exp_to_next_level:
            self.level_up()
    
    def level_up(self):
        self.current_exp -= self.exp_to_next_level
        self.current_level += 1
        self.skill_points += 1
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        self.on_level_up()
    
    def on_level_up(self):
        self.player.health_component.max_health += 10
        self.player.health_component.heal(10)
        print(f"🎉 Уровень UP! Теперь уровень {self.current_level}")