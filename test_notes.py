import unittest
import main


def run_assert_tests():
    print("Запуск тестів 'assert'...")

    main.notes = []
    main.next_id = 1

    note = {"id": 1, "title": "План", "text": "Купити хліб", "date": "24.05.2026 12:00"}
    main.notes.append(note)

    assert len(main.notes) == 1, "Помилка: Нотатка не була додана до списку!"
    assert main.notes[0]["title"] == "План", "Помилка: Заголовок нотатки не збігається!"

    query = "план"
    results = [n for n in main.notes if query.lower() in n["title"].lower()]

    assert len(results) == 1, "Помилка: Пошук не знайшов нотатку в нижньому регістрі!"

    nid = 1
    for i, n in enumerate(main.notes):
        if n["id"] == nid:
            main.notes.pop(i)

    assert len(main.notes) == 5, "Помилка: Очікувалось 5 нотаток після видалення!"
    print("Усі тести 'assert' успішно пройдено!\n")


class TestNotesApp(unittest.TestCase):

    def setUp(self):
        main.notes = []
        main.next_id = 1

    def test_add_note_structure(self):
        test_note = {"id": main.next_id, "title": "Лекція", "text": "Тестування ПЗ", "date": "24.05.2026"}
        main.notes.append(test_note)

        self.assertEqual(len(main.notes), 1)
        self.assertIn("id", main.notes[0])
        self.assertEqual(main.notes[0]["text"], "Тестування ПЗ")

    def test_search_by_text(self):
        main.notes.append({"id": 1, "title": "Шопінг", "text": "Купити новий монітор", "date": "24.05.2026"})

        query = "телевізор"
        results = [n for n in main.notes if query.lower() in n["text"].lower()]

        self.assertTrue(len(results) > 0, "Нотатку не знайдено за текстом опису")
        self.assertEqual(results[0]["id"], 1)

    def test_delete_non_existent_note(self):
        main.notes.append({"id": 1, "title": "Тест", "text": "Просто текст", "date": "24.05.2026"})

        nid_to_delete = 999
        found = any(n["id"] == nid_to_delete for n in main.notes)

        self.assertFalse(found, "Помилка: Знайдено ідентифікатор, якого не існує")


if __name__ == "__main__":
    run_assert_tests()

    unittest.main()