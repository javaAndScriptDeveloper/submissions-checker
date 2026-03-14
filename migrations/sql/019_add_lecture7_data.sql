-- Migration: 019_add_lecture7_data
-- Description: Seed lecture knowledge for lab 7 (exception handling)
INSERT INTO lecture_knowledge (lab_id, content) VALUES (7, $content$
Обробка винятків (try, except, finally)
Винятки — це помилки, що виникають під час виконання програми. Для їх перехоплення та безпечної обробки використовується конструкція try-except. Це запобігає аварійному завершенню програми.

Блок try містить код, який може викликати помилку. Блок except вказує, як реагувати на конкретний тип помилки (наприклад, ZeroDivisionError, ValueError, FileNotFoundError).

Додаткові блоки:
Блок else виконується, якщо в try не виникло жодної помилки. Блок finally виконується завжди, незалежно від наявності помилок (корисно для звільнення ресурсів або закриття з'єднань).

try:
    x = int(input('Введіть число: '))
    res = 10 / x
except ZeroDivisionError:
    print('Помилка: ділення на нуль!')
except ValueError:
    print('Помилка: введено не число!')
else:
    print('Результат:', res)
finally:
    print('Перевірка завершена.')
$content$)
ON CONFLICT (lab_id) DO UPDATE SET content = EXCLUDED.content;
