import csv
import json

data = [
    ["Имя", "Возраст", "Город", "Должность", "Зарплата"],
    ["Анна", 28, "Москва", "Аналитик", 95000],
    ["Борис", 34, "Москва", "Разработчик", 140000],
    ["Вера", 25, "Санкт-Петербург", "Аналитик", 85000],
    ["Глеб", 40, "Новосибирск", "Разработчик", 130000],
    ["Дарья", 31, "Москва", "Менеджер", 110000],
    ["Евгений", 29, "Санкт-Петербург", "Разработчик", 125000],
    ["Зоя", 27, "Новосибирск", "Менеджер", 100000],
    ["Игорь", 33, "Казань", "Разработчик", 120000],
    ["Людмила", 26, "Казань", "Аналитик", 80000],
    ["Максим", 36, "Москва", "Разработчик", 150000]
]

with open('employees_with_salary.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data)


avg_age_by_city = {} # Средний вораст в каждом городе
total_salary_by_position = {} #Сумма ЗП по каждой должности
count_by_city = {} #кол-во сотрудников в каждом городе
age_sum_by_city = {} #Сумма воростов в каждом городе

with open('employees_with_salary.csv', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        city = row['Город']
        age = int(row['Возраст'])
        position = row['Должность']
        salary = float(row['Зарплата'])

        age_sum_by_city[city] = age_sum_by_city.get(city, 0) + age
        count_by_city[city] = count_by_city.get(city, 0) + 1
        total_salary_by_position[position] = total_salary_by_position.get(position, 0.0) + salary

for city in age_sum_by_city:
    avg_age_by_city[city] = round(age_sum_by_city[city] / count_by_city[city])


res = {
    "Cредний_возраст_по_городам": avg_age_by_city,
    "Cумма_зарплат_по_должностям": total_salary_by_position,
    "Количество_по_городам": count_by_city
}

with open('stats.json', 'w', encoding='utf-8') as file:
    json.dump(res, file, ensure_ascii=False, indent=2)
