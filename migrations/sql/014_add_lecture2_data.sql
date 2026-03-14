-- Migration: 014_add_lecture2_data
-- Description: Seed lecture knowledge for lab 2 (conditions, while, for loops)
INSERT INTO lecture_knowledge (lab_id, content) VALUES (2, $content$
Умови (if, elif, else)
Синтаксис дозволяє створювати розгалуження будь-якої складності. Для створення порожніх блоків (заглушок) використовується оператор pass.
x = int(input("Введіть х="))
if x >= 0:
    y = x ** 0.5
elif x == -1:
    y = 0
else:
    y = x ** 2

Цикл while:
Виконує тіло циклу, поки умова є істинною. Підтримує переривання break та гілку else, яка виконується, якщо цикл завершився природним шляхом (без break).
i = 0
while i < 3:
    print(i)
    i += 1
else:
    print("Кінець циклу")

Цикл for та генерація послідовностей:
Функція range(start, end, step) використовується для створення числових послідовностей. Функція zip() дозволяє ітерувати відразу за кількома послідовностями одночасно. Також підтримується синтаксис List Comprehension ([ВИРАЗ for ЕЛЕМЕНТ in ІТЕРАЦІЙНИЙ_ОБ'ЄКТ if УМОВА]).
for number in numbers:
    print(number)
for day, drink in zip(days, drinks):
    print(day, drink)
number_list = [number for number in range(1, 6) if number % 2 == 1]
$content$)
ON CONFLICT (lab_id) DO UPDATE SET content = EXCLUDED.content;
