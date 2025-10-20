import random
import time
import sys
from data import *

def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def show_status():
    slow_print(f"\n--- День {player_state['day']} ---")
    slow_print(f"Еда: {player_state['food']}")
    slow_print(f"Вода: {player_state['water']}")
    slow_print(f"Мораль: {player_state['morale']}")
    slow_print(f"Население: {player_state['population']}")
    slow_print(f"Болты: {player_state['bolts']}")
    if expeditions:
        slow_print(f"Активные вылазки: {len(expeditions)}")
        for exp in expeditions:
            if exp["day"] > player_state["day"]:
                slow_print(f"  - вернётся на день {exp['day']} с {len(exp['participants'])} участниками")

def assign_jobs():
    slow_print(f"\n--- Назначение работ ---")
    if player_state["population"] == 0:
        slow_print("Нет жителей для назначения работы.")
        return

    while True:
        slow_print("\nСписок жителей:")
        for i in range(player_state["population"]):
            current_job = jobs.get(i, "житель")
            on_exp = any(i in exp["participants"] for exp in expeditions if exp["day"] > player_state["day"])
            status = f" ({'в вылазке' if on_exp else 'в бункере'})"
            slow_print(f"  #{i}: {current_job}{status}")

        try:
            selected_id = int(input(f"\nВведите ID жителя (0-{player_state['population'] - 1}, '-1'-выход): "))
        except ValueError:
            slow_print("Неверный ввод. Введите число.")
            continue

        if selected_id >= player_state["population"]:
            slow_print("Неверный ID жителя.")
            continue
        if selected_id < 0:
            slow_print("Выход из назначения работ.")
            break

        on_exp = any(selected_id in exp["participants"] for exp in expeditions if exp["day"] > player_state["day"])
        if on_exp:
            slow_print(f"Житель #{selected_id} сейчас в вылазке, нельзя изменить работу.")
            continue

        current_job = jobs.get(selected_id, "житель")
        slow_print(f"Текущая работа для #{selected_id}: {current_job}")
        slow_print("Доступные работы: житель, добытчик еды, добытчик воды")
        new_job = input(f"Введите новую работу для #{selected_id}: ").strip()

        if new_job in ["житель", "добытчик еды", "добытчик воды"]:
            jobs[selected_id] = new_job
            slow_print(f"#{selected_id} теперь: {new_job}")
        else:
            slow_print(f"Неверная работа '{new_job}', остаётся: {current_job}")

        again = input("\nХотите назначить работу ещё кому-нибудь? (да/нет): ").strip().lower()
        if again not in ["да", "д"]:
            slow_print("Выход из назначения работ.")
            break

def do_daily_job_production():
    active_ids = [i for i in range(player_state["population"]) if not any(i in exp["participants"] for exp in expeditions if exp["day"] > player_state["day"])]
    food_workers = [pid for pid in active_ids if jobs.get(pid, "житель") == "добытчик еды"]
    water_workers = [pid for pid in active_ids if jobs.get(pid, "житель") == "добытчик воды"]

    food_produced = len(food_workers) * random.randint(1, 3)
    water_produced = len(water_workers) * random.randint(1, 3)

    if food_produced > 0:
        player_state["food"] += food_produced
        slow_print(f"Добыто еды: +{food_produced}")
    if water_produced > 0:
        player_state["water"] += water_produced
        slow_print(f"Добыто воды: +{water_produced}")

def repair_system():
    slow_print("\nДоступные для ремонта системы:")
    broken_systems = [sys for sys, working in systems.items() if not working and sys != "auto_water"]
    if not broken_systems:
        slow_print("Нет сломанных систем.")
        return

    for i, sys in enumerate(broken_systems):
        slow_print(f"{i + 1}. {sys.replace('_', ' ').title()} (стоимость: 10 болтов)")

    choice = input("Выберите систему для ремонта (введите номер или '0', чтобы выйти): ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(broken_systems):
            system = broken_systems[idx]
            if player_state["bolts"] >= 10:
                player_state["bolts"] -= 10
                systems[system] = True
                slow_print(f"{system.replace('_', ' ').title()} отремонтирована за 10 болтов.")
            else:
                slow_print("Недостаточно болтов для ремонта.")
        elif choice != "0":
            slow_print("Неверный выбор.")

def mission():
    available_ids = [i for i in range(player_state["population"]) if
                     not any(i in exp["participants"] for exp in expeditions if exp["day"] > player_state["day"])]

    if not available_ids:
        slow_print("Нет доступных жителей для вылазки (все в походе или отсутствуют).")
        return

    slow_print(f"Доступные для вылазки: {available_ids}")
    participants_input = input("Введите ID жителей через запятую (например, 0,1): ").strip()
    try:
        participants = [int(x.strip()) for x in participants_input.split(",")]
    except ValueError:
        slow_print("Неверный ввод. Введите числа, разделённые запятой.")
        return

    for pid in participants:
        if pid not in available_ids:
            slow_print(f"Житель #{pid} не может участвовать в вылазке.")
            return

    if not participants:
        slow_print("Нет участников для вылазки.")
        return

    try:
        duration = int(input("Введите длительность вылазки (1-5 дней): "))
    except ValueError:
        slow_print("Неверный ввод. Длительность по умолчанию: 1 день.")
        duration = 1

    if duration < 1:
        duration = 1
    elif duration > 5:
        duration = 5

    food_needed = int(len(participants) * duration * 1.5)
    if player_state["food"] < food_needed:
        slow_print(f"Недостаточно еды для вылазки. Требуется: {food_needed}, есть: {player_state['food']}.")
        return

    player_state["food"] -= food_needed
    slow_print(f"Вылазка отправлена с {len(participants)} участниками на {duration} дней.")
    slow_print(f"Потрачено еды на вылазку: {food_needed}")

    expeditions.append({
        "day": player_state["day"] + duration,
        "participants": participants,
        "success": None,
        "resources": {},
        "infected": []
    })

def build_upgrade():
    available_upgrades = {k: v for k, v in upgrades.items() if not systems[k]}
    if not available_upgrades:
        slow_print("Нет доступных улучшений.")
        return

    slow_print("\nДоступные улучшения:")
    for key, data in available_upgrades.items():
        slow_print(f" - {data['name']} (стоимость: {data['cost']} болтов)")

    choice = input("Введите название улучшения (или '0', чтобы выйти): ").strip()
    if choice.lower() == "автоматический генератор воды":
        key = "auto_water"
        if player_state["bolts"] >= upgrades[key]["cost"]:
            player_state["bolts"] -= upgrades[key]["cost"]
            systems[key] = True
            slow_print("Автоматический генератор воды построен! Вода теперь восстанавливается каждый день.")
        else:
            slow_print("Недостаточно болтов для постройки.")

def process_expeditions():
    for exp in expeditions[:]:
        if exp["day"] == player_state["day"]:
            base_chance = base_event_chance
            morale_factor = player_state["morale"] / 100
            success = random.random() < (base_chance * morale_factor)

            if success:
                found_bolts = random.randint(3, 8)
                found_food = random.randint(5, 10)
                exp["success"] = True
                exp["resources"] = {"bolts": found_bolts, "food": found_food}
                slow_print(f"Вылазка вернулась успешно! Найдено: {found_bolts} болтов и {found_food} еды.")
                player_state["bolts"] += found_bolts
                player_state["food"] += found_food
            else:
                exp["success"] = False
                slow_print("Вылазка провалилась. Никаких ресурсов не найдено.")

            for pid in exp["participants"]:
                if random.random() < infection_chance:
                    exp["infected"].append(pid)
                    slow_print(f"Житель #{pid} заражён после вылазки!")

            expeditions.remove(exp)

def do_daily_event():
    event = random.choice(events)
    slow_print(f"[СОБЫТИЕ] {event}")

    if event == "Протечка воды в трубах!":
        player_state["water"] -= 10
        slow_print("Вода потеряна: -10")

    elif event == "Крысы съели часть еды!":
        player_state["food"] -= 10
        slow_print("Еда потеряна: -10")

    elif event == "Найден тайник с болтами!":
        player_state["bolts"] += 20
        slow_print("Найдено: +20 болтов")

    elif event == "Появился новый выживший!":
        if random.random() > 0.4:
            player_state["population"] += 1
            jobs[player_state["population"] - 1] = "житель"
            slow_print("Новый выживший принят в бункер.")
        else:
            slow_print("Выживший ушёл.")

    elif event == "Кто-то заболел!":
        player_state["morale"] -= 10
        slow_print("Мораль снижена: -10")

    elif event == "Получено радио сообщение о спасении!":
        slow_print("Радио: 'Последствия бедствия будут устранены через 365 дней. Выживайте.'")
        player_state["year_known"] = True

    elif event == "Появился торговец!":
        slow_print("Торговец предлагает обменять 10 болтов на 15 еды или 15 воды.")
        choice = input("Что берёте? (еда/вода/ничего): ").strip().lower()
        if choice in ["еда", "вода"] and player_state["bolts"] >= 10:
            player_state["bolts"] -= 10
            if choice == "еда":
                player_state["food"] += 15
                slow_print("Вы получили 15 еды.")
            else:
                player_state["water"] += 15
                slow_print("Вы получили 15 воды.")
        else:
            slow_print("Вы ничего не взяли.")

    elif event == "Пришёл дезертир!":
        slow_print("Дезертир предлагает обменять информацию на болты.")
        choice = input("Дать 5 болтов за информацию? (да/нет): ").strip().lower()
        if choice == "да" and player_state["bolts"] >= 5:
            player_state["bolts"] -= 5
            info = random.choice(["Найден тайник с 20 болтами!", "Система фильтра отремонтирована бесплатно!"])
            slow_print(f"Информация: {info}")
            if "20 болтами" in info:
                player_state["bolts"] += 20
            elif "фильтра" in info:
                systems["air_filter"] = True
        else:
            slow_print("Вы не дали болты.")

    elif event == "Сломалась система фильтрации!":
        systems["air_filter"] = False
        slow_print("Система фильтрации сломалась! Мораль будет снижаться каждый день.")

    elif event == "Сломались трубы!":
        systems["pipes"] = False
        slow_print("Трубы сломались! Вода тратится быстрее.")

def consume_resources():
    base_food_consumption = player_state["population"]
    base_water_consumption = player_state["population"]

    if not systems["pipes"]:
        base_water_consumption *= 2

    player_state["food"] -= base_food_consumption
    player_state["water"] -= base_water_consumption

    if not systems["air_filter"]:
        player_state["morale"] -= 2

    if systems["auto_water"]:
        player_state["water"] += 5

    for res in ["food", "water", "morale"]:
        if player_state[res] < 0:
            player_state[res] = 0

    slow_print(f"Население: {player_state['population']} человек")
    slow_print(f"Потребление: -{base_food_consumption} еды, -{base_water_consumption} воды")

def check_alive():
    for res in critical_resources:
        if player_state[res] <= 0:
            slow_print(f"Все умерли от {res}...")
            return False
    return True

def bunker_game():
    slow_print("Добро пожаловать в Бункер!")
    slow_print("Выживайте, управляйте ресурсами, принимайте решения.")

    while True:
        show_status()

        slow_print("\nДоступные действия:")
        for i, action in enumerate(actions):
            slow_print(f"{i + 1}. {action}")

        choice = input("Выберите действие: ")

        if choice == "1":
            slow_print(f"Системы:")
            slow_print(f"  - трубы — {'ок' if systems['pipes'] else 'сломаны'}")
            slow_print(f"  - генератор — {'ок' if systems['generator'] else 'сломан'}")
            slow_print(f"  - фильтр — {'ок' if systems['air_filter'] else 'сломан'}")
            slow_print(f"  - автогенератор — {'ок' if systems['auto_water'] else 'нет'}")
        elif choice == "2":
            repair_system()
        elif choice == "3":
            mission()
        elif choice == "4":
            assign_jobs()
        elif choice == "5":
            build_upgrade()
        elif choice == "6":
            slow_print("День завершён.")

            process_expeditions()

            if random.randint(0, 2) < 1:
                do_daily_event()

            do_daily_job_production()
            consume_resources()
            if not check_alive():
                slow_print(f"\nВы не выжили до дня {player_state['day']}.")
                break
            player_state["day"] += 1

            if player_state["year_known"] and player_state["day"] > 365:
                slow_print("\n Поздравляем! Вы выжили целый год!")
                slow_print("Бедствие окончено, спасательные отряды эвакуируют выживших.")
                slow_print("Вы спасены! Конец игры.")
                break
        else:
            slow_print("Неверный выбор. Попробуйте снова.")

    slow_print("\nИгра окончена.")

if __name__ == "__main__":
    bunker_game()