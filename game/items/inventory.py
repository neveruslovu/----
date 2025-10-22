"""
Система инвентаря игрока
"""

class Inventory:
    def __init__(self, capacity=20):
        self.capacity = capacity
        self.items = []
        self.gold = 0
        
    def add_item(self, item):
        """Добавить предмет в инвентарь"""
        if len(self.items) < self.capacity:
            # Проверяем можно ли стакать
            for inv_item in self.items:
                if inv_item.name == item.name and inv_item.stackable:
                    inv_item.quantity += item.quantity
                    return True
            
            # Добавляем новый предмет
            self.items.append(item)
            return True
        return False
    
    def remove_item(self, item):
        """Удалить предмет из инвентаря"""
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def use_item(self, item_index):
        """Использовать предмет по индексу"""
        if 0 <= item_index < len(self.items):
            item = self.items[item_index]
            # Здесь будет логика использования предмета
            if item.consumable:
                item.quantity -= 1
                if item.quantity <= 0:
                    self.remove_item(item)
            return True
        return False
    
    def get_save_data(self):
        """Получить данные для сохранения"""
        return {
            "gold": self.gold,
            "items": [item.get_save_data() for item in self.items]
        }