-- Migration: 015_add_lecture3_data
-- Description: Seed lecture knowledge for lab 3 (lists, tuples, dicts)
INSERT INTO lecture_knowledge (lab_id, content) VALUES (3, $content$
Списки (list)
Змінювані структури даних, що створюються як [] або list(). Важливо пам'ятати різницю між присвоєнням посилання (b = a) та фактичним копіюванням списку (b = a.copy(), b = list(a), або b = a[:]).
letters = ['a', 'b', 'c', 'd', 'e']
letters.append('f')         # Додавання елемента
letters.extend(['g', 'h'])  # Розширення іншим списком
letters.insert(2, 'm')      # Вставлення за індексом
del letters[2]              # Видалення за індексом
letters.remove('b')         # Видалення по значенню
deleted_val = letters.pop(1) # Повертає і видаляє елемент
idx = letters.index('d')    # Знайти індекс елемента
letters.sort(reverse=True)  # Сортування списку (зміна поточного)

Кортежі (tuple)
Незмінювані аналоги списків. Створюються через () або tuple(). Кортеж з одного елемента обов'язково потребує коми: 'Alex',. Завдяки кортежам можливе зручне розпакування та обмін значень змінних.
name_tuple = ('Alex', 'Helen', 'Olga')
a, b, c = name_tuple # Розпакування
a, b = b, a          # Швидкий обмін значень

Словники (dict)
Колекції пар "ключ: значення". Створюються через {} або dict(). Якщо звернутись до неіснуючого ключа напряму dict[key], буде помилка KeyError. Безпечний спосіб — метод .get().
dict_1 = {1: "a", 3: "c", 4: "d"}
val = dict_1.get('2', 'Not a dict') # Безпечне отримання значення
dict_1[2] = "b"            # Додавання або зміна елемента
dict_1.update(e=3, d=4)    # Масове оновлення
del dict_1[1]              # Видалення елемента
dict_1.clear()             # Видалення всіх елементів
dict_1.keys()              # Ключі
dict_1.values()            # Значення
dict_1.items()             # Пари (ключ, значення)
$content$)
ON CONFLICT (lab_id) DO UPDATE SET content = EXCLUDED.content;
