"""
Классы предметов для игры
"""

class Item:
    def __init__(self, name, item_type, value=0, stackable=True, consumable=False):
        self.name = name
        self.type = item_type  # "weapon", "potion", "armor", "misc"
        self.value = value
        self.stackable = stackable
        self.consumable = consumable
        self.quantity = 1
        
    def use(self, player):
        """Использовать предмет"""
        if self.type == "potion":
            if self.name == "Health Potion":
                player.health_component.heal(50)
                return True
        return False
    
    def get_save_data(self):
        """Получить данные для сохранения"""
        return {
            "name": self.name,
            "type": self.type,
            "quantity": self.quantity
        }

class Weapon(Item):
    def __init__(self, name, damage, attack_speed=1.0):
        super().__init__(name, "weapon")
        self.damage = damage
        self.attack_speed = attack_speed

class Potion(Item):
    def __init__(self, name, heal_amount=50):
        super().__init__(name, "potion", consumable=True)
        self.heal_amount = heal_amount
    
    def use(self, player):
        player.health_component.heal(self.heal_amount)
        return True