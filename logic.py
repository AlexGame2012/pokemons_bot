from random import randint
import requests

class Pokemon:
    pokemons = {}
    
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer   
        self.pokemon_number = randint(1, 1000)
        
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            self.name = data['name']
            self.img_url = data['sprites']['front_default']
            
            # Берем HP и силу напрямую из API
            for stat in data['stats']:
                if stat['stat']['name'] == 'hp':
                    self.hp = stat['base_stat']
                if stat['stat']['name'] == 'attack':
                    self.power = stat['base_stat']
            
            # Получаем типы покемона
            self.types = [type_info['type']['name'] for type_info in data['types']]
            
        else:
            # Fallback значения если API не доступно
            self.name = 'Pikachu'
            self.img_url = ''
            self.hp = randint(30, 40)
            self.power = randint(4, 10)
            self.types = ['electric']

        Pokemon.pokemons[pokemon_trainer] = self

    def get_info(self):
        types_str = ", ".join(self.types)
        info_text = f"""
🎉 Твой покемон!

📊 {self.name.capitalize()}
❤️ HP: {self.hp}
⚡ Сила: {self.power}
🎨 Тип: {types_str}

"""
        return self.img_url, info_text
        

    def info(self):
        types_str = ", ".join(self.types)
        return (
            f"📊 Имя: {self.name.capitalize()}\n"
            f"❤️ HP: {self.hp}\n"
            f"⚡ Сила: {self.power}\n"
            f"🎨 Тип: {types_str}\n"
            f"👾 Владелец: @{self.pokemon_trainer}"
        )
        
    def attack(self, enemy):
        # Вычисляем разницу в силе
        power_difference = self.power - enemy.power
        
        if power_difference > 0:
            # Если наша сила больше - отнимаем HP у противника на величину разницы
            damage = power_difference
            enemy.hp -= damage
            if enemy.hp <= 0:
                enemy.hp = 0
                return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! Разница в силе: {damage}"
            else:
                return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}! Разница в силе: {damage}. Здоровье: @{self.pokemon_trainer}: {self.hp} / @{enemy.pokemon_trainer}: {enemy.hp}"
        else:
            # Если сила противника больше или равна - наш покемон получает урон
            damage = abs(power_difference)
            self.hp -= damage
            if self.hp <= 0:
                self.hp = 0
                return f"Победа @{enemy.pokemon_trainer} над @{self.pokemon_trainer}! Разница в силе: {damage}"
            else:
                return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}! Разница в силе: {damage}. Здоровье: @{self.pokemon_trainer}: {self.hp} / @{enemy.pokemon_trainer}: {enemy.hp}"