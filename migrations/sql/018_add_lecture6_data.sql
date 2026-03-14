-- Migration: 018_add_lecture6_data
-- Description: Seed lecture knowledge for lab 6 (JSON, CSV, Pandas)
INSERT INTO lecture_knowledge (lab_id, content) VALUES (6, $content$
Робота з форматами даних: JSON, CSV та основи Pandas
У сучасній розробці програми постійно обмінюються даними. Найпопулярніші формати для цього — JSON (JavaScript Object Notation) та CSV (Comma-Separated Values).

Модуль json:
Формат JSON ідеально підходить для збереження словників та списків Python.
- json.dumps(obj) — серіалізація: перетворює об'єкт Python на рядок JSON. Часто використовується параметр indent=4 для красивого форматування.
- json.loads(string) — десеріалізація: перетворює рядок JSON на об'єкт Python (словник або список).
- json.dump(obj, file) — записує об'єкт безпосередньо у відкритий текстовий файл. Для збереження кирилиці обов'язково треба вказувати ensure_ascii=False.
- json.load(file) — зчитує об'єкт із відкритого файлу.

Модуль csv:
Призначений для роботи з табличними даними (де значення розділені комами або крапкою з комою).
- csv.reader(file) — читає файл по рядках, кожен рядок стає списком рядків (list of strings).
- csv.writer(file) — створює об'єкт для запису. Метод .writerow(list) записує один рядок, .writerows(list_of_lists) — одразу кілька.
- csv.DictReader та csv.DictWriter — дозволяють працювати з рядками як зі словниками, де ключами виступають назви колонок.

Основи Pandas:
Pandas — це найпотужніша зовнішня бібліотека для аналізу даних. Головна структура — DataFrame (двовимірна таблиця).
- pd.read_csv('file.csv') — миттєво завантажує таблицю в пам'ять.
- df.head(n) — виводить перші n рядків таблиці.
- df.to_excel('file.xlsx', index=False) — конвертує та зберігає дані у форматі Excel.

import json
import csv

# Робота з JSON
data = {"user": "Alex", "role": "admin", "skills": ["Python", "SQL"]}
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# Робота з CSV (запис)
with open('users.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Age", "City"])
    writer.writerow(["Helen", 25, "Kyiv"])
$content$)
ON CONFLICT (lab_id) DO UPDATE SET content = EXCLUDED.content;
