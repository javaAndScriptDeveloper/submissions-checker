-- Migration: 016_add_lecture4_data
-- Description: Seed lecture knowledge for lab 4 (functions, scope, recursion)
INSERT INTO lecture_knowledge (lab_id, content) VALUES (4, $content$
Функції (def, return) та параметри
Функції ініціалізуються ключовим словом def. Вони можуть приймати позиційні або іменовані аргументи, а також мати значення за замовчуванням.
def summa(x, y=2): # y має значення за замовчуванням
    return x + y

def print_args(*args, **kwargs):
    print('Позиційні:', args)   # Повертає кортеж
    print('Іменовані:', kwargs) # Повертає словник

print_args(1, 2, c=3)

Область видимості
Змінні всередині функції є локальними. Для зміни глобальної змінної всередині функції потрібно використовувати ключове слово global.
x = 50
def func():
    global x # Вказуємо, що х - глобальна змінна
    x = 2

Рекурсія та вкладені функції
Функції можуть бути вкладеними одна в одну (внутрішні функції). Рекурсія — це коли функція викликає саму себе. Рекурсивна функція обов'язково повинна мати базову умову виходу, інакше виникне помилка.
def factorial(n):
    if n > 0:
        return n * factorial(n - 1)
    else:
        return 1

Модульність
У Python доступні вбудовані функції, наприклад abs(). Для розширених математичних операцій використовується модуль math (math.sqrt()) та модуль random для генерації випадкових чисел.
$content$)
ON CONFLICT (lab_id) DO UPDATE SET content = EXCLUDED.content;
