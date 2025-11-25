import random
import os

if not os.path.exists('stats'):
    os.makedirs('stats')

razm_pole = 3
pole = []
mode = None
hod = random.choice(["X", "O"])
now = 1
game = True


def oshibka(x):
    match x:
        case "001":
            print("Код ошибки #001 - Выбран неверный размер поля")
        case "002":
            print("Код ошибки #002 - При выборе размера поля было введено не число")
        case "003":
            print("Код ошибки #003 - Неверный формат выбора места хода")
        case "004":
            print("Код ошибки #004 - Выбранное место за пределами поля")
        case "005":
            print("Код ошибки #005 - Выбранное место уже занято")


def save(winner_str, now):
    z = input("Назовите как-нибудь сохранение (например: save1): ")
    file_name = "stats/" + z + ".txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(f'выйграл {winner_str} на {now} ходу\n')


def check_win():
    global pole, razm_pole, hod
    for stolbik in range(razm_pole):
        if all(pole[stolbik][colonka] == hod for colonka in range(razm_pole)):
            return True
    for colonka in range(razm_pole):
        if all(pole[stolbik][colonka] == hod for stolbik in range(razm_pole)):
            return True
    if all(pole[i][i] == hod for i in range(razm_pole)):
        return True
    if all(pole[i][razm_pole - 1 - i] == hod for i in range(razm_pole)):
        return True
    return False


def create_pole():
    global razm_pole, pole
    try:
        razm_pole = int(input("Для начала игры выберите размер поля (3-9):\n"))
        if razm_pole < 3 or razm_pole > 9:
            oshibka("001")
            create_pole()
        else:
            pole = [["." for z in range(razm_pole)] for z in range(razm_pole)]
    except:
        oshibka("002")
        create_pole()


def pokaz():
    global pole
    x = 0
    print("   ", end="")
    for i in range(1, len(pole) + 1):
        print(str(i) + "  ", end="")
    print()
    for i in pole:
        x += 1
        print(str(x) + "  ", end="")
        for z in i:
            print(z + "  ", end="")
        print()


def smena_hoda():
    global hod
    match hod:
        case "X":
            hod = "O"
        case "O":
            hod = "X"


def robot_hod():
    global pole, razm_pole
    svobodnye = []
    for i in range(razm_pole):
        for j in range(razm_pole):
            if pole[i][j] == ".":
                svobodnye.append((i, j))
    if svobodnye:
        y, x = random.choice(svobodnye)
        pole[y][x] = "O"
        print(f"\nРобот сделал ход: {y + 1} {x + 1}")


def hodi():
    global hod, pole, razm_pole, now, game, mode
    while game:
        if now > razm_pole * razm_pole:
            game = False
            break

        print(f"Ход номер #{now}\n")
        pokaz()

        if mode == "2" and hod == "O":
            robot_hod()
        else:
            vibor = input(f"\nХодит '{hod}', выберите место хода (например: 1 2):\n")
            if len(vibor) != 3:
                oshibka("003")
                continue
            try:
                z, x = vibor.split(" ")
                z = int(z)
                x = int(x)
            except:
                oshibka("003")
                continue

            if z < 1 or x < 1 or z > razm_pole or x > razm_pole:
                oshibka("004")
                continue
            elif pole[z - 1][x - 1] != ".":
                oshibka("005")
                continue
            else:
                pole[z - 1][x - 1] = hod

        if check_win():
            if mode == "2" and hod == "O":
                winner_str = "робот"
            else:
                winner_str = f"игрок {hod}"

            pokaz()
            print(f"\n{winner_str} победил на {now} ходу!")

            if input("\nХотите сыграть ещё? (1-Да, 0-Нет):\n") == "1":
                save(winner_str, now)
                print("Счет успешно сохранен")
                start_game()
            else:
                save(winner_str, now)
                print("Игра окончена, счет сохранен")
                game = False
                break

        now += 1
        smena_hoda()

    if not game and now == razm_pole * razm_pole:
        pokaz()
        print("\nНичья!")


def start_game():
    global mode, hod, now, game
    now = 1
    game = True

    create_pole()

    while True:
        mode = input("\nВыберите режим игры:\n1 - Два игрока\n2 - Против робота\nВаш выбор: ")
        if mode in ["1", "2"]:
            break
        print("Неверный выбор! Попробуйте снова.")

    if mode == "2":
        hod = "X"
    else:
        hod = random.choice(["X", "O"])

    hodi()


if __name__ == "__main__":
    start_game()