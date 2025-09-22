check_list = ["+", "-", "*", "/", "//", "%", "**","==","!=","<",">","<=",">="]
check_list1=["and","or","not"]

def bol(a):
    if a.lower() == "true": return True
    elif a.lower() == "false": return False

def innt(a,op):
    if op in check_list:
        try:
            a = int(a)
            return a
        except ValueError:
            return "error"

def vivod(a,op,b,ans):
    if op in check_list and isinstance(ans,bool):
        if ans == True: print(f"{a} {op} {b} - верно")
        elif ans == False: print(f"{a} {op} {b} - неверно")
    elif op in check_list and ans is not bool:print(f"{a} {op} {b} = {ans}")
    elif op in check_list1:
        if op == "not":print(f"not {a} = {not bol(a)}\nnot {b} = {not bol(b)}")
        else:print(a, op ,b,"=",ans)
    else:alert("vivod")

def alert(warn):
    if warn == "end":alert="Работа калькулятора завершена"
    elif warn == "int": alert = "ERROR: Было введено не число"
    elif warn == "noop": alert = "ERROR: Операция введена не корректно"
    elif warn == "vivod":alert = "ERROR: Ошибка вывода итога"
    elif warn == "zero": alert = "ERROR: Деление на ноль"
    print(f"""
----------------------------------------------
       {alert}
----------------------------------------------
""")


while True:
    a = input("Введите 1е значение\n")
    if a == "None": alert("end"); break
    op = input("""
------------------------------
  1.Арифметические операторы
    + Сложение
    - Вычитание
    * Умножение
    / Деление
    // Целочисленное деление
    % Остаток от деления
    ** Возведение в степень
------------------------------
  2.Операторы сравнения
    == Равно
    != Не равно
    > Больше
    < Меньше
    >= Больше или равно
    <= Меньше или равно
------------------------------
  3.Логические операторы
    and Логическое И
    or Логическое ИЛИ
    not Логическое НЕ
------------------------------

Выберете операцию:
""")
    if op not in check_list and op not in check_list1:alert("noop");continue
    b = input("Введите 2е значение (для завершения работы введите None)\n")
    if b == "None":alert("end"); break

    if op in check_list:
        a = innt(a,op)
        b = innt(b,op)
        if a == "error" or b == "error":alert("int"); continue
    if op == "+":ans=a+b
    elif op == "-":ans=a-b
    elif op == "*":ans=a*b
    elif op == "/":
        if b == 0:alert("zero");continue
        else:ans=a/b
    elif op == "//":
        if b == 0:alert("zero");continue
        else:ans=a//b
    elif op == "%":
        if b == 0:alert("zero");continue
        else:ans=a%b
    elif op == "**":ans=a**b
    elif op == "==": ans= a==b
    elif op == "!=": ans= a!=b
    elif op == ">": ans= a>b
    elif op == "<": ans= a<b
    elif op == ">=": ans= a>=b
    elif op == "<=": ans= a<=b
    elif op == "and":ans = bol(a) and bol(b)
    elif op == "or":ans = bol(a) or bol(b)
    elif op == "not": ans="Ну так то оно не нужно тут ;)"
    vivod(a, op, b, ans)

