player_state = {
    "food": 50,
    "water": 50,
    "morale": 60,
    "population": 2,
    "day": 1,
    "bolts": 20,
    "year_known": False
}

systems = {
    "pipes": True,
    "generator": True,
    "air_filter": True,
    "auto_water": False
}

critical_resources = {"food", "water"}

jobs = {
    0: "житель",
    1: "житель"
}

expeditions = []

upgrades = {
    "auto_water": {"name": "Автоматический генератор воды", "cost": 50, "effect": lambda: player_state.update({"water": player_state["water"] + 5})}
}

actions = [
    "Проверить статус систем",
    "Починить систему",
    "Отправить вылазку за ресурсами",
    "Назначить работу населению",
    "Построить улучшение",
    "Завершить день"
]

events = [
    "Протечка воды в трубах!",
    "Крысы съели часть еды!",
    "Найден тайник с болтами!",
    "Появился новый выживший!",
    "Кто-то заболел!",
    "Получено радио сообщение о спасении!",
    "Появился торговец!",
    "Пришёл дезертир!",
    "Сломалась система фильтрации!",
    "Сломались трубы!"
]

base_event_chance = 0.5
infection_chance = 0.3