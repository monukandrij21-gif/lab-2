logins = ["Andrii", "Petro", "Maksim", "Vlad"]
passwords = ["1234", "3333", "1111", "2222"]

grades = [
    [10, 8, 7, 12, 5],
    [4, 3, 8, 6, 2],
    [9, 10, 12, 7, 11],
    [3, 5, 4, 8, 2]
]

login = input("Введіть логін: ")
password = input("Введіть пароль: ")

if login == "Andrii" and password == "1234":
    user_grades = grades[0]

elif login == "Petro" and password == "3333":
    user_grades = grades[1]

elif login == "Maksim" and password == "1111":
    user_grades = grades[2]

elif login == "Vlad" and password == "2222":
    user_grades = grades[3]

else:
    print("Неправильний логін або пароль!")
    user_grades = []

if user_grades:
    print("Вхід успішний!")
    print("Ваші оцінки:", user_grades)

    good = 0
    bad = 0

    for grade in user_grades:
        if grade >= 7:
            good = good + 1
        else:
            bad = bad + 1

    print("Задовільних оцінок:", good)
    print("Незадовільних оцінок:", bad)