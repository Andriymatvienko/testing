import pytest
import main


@pytest.fixture(autouse=True)
def clean_database():
    main.notes = []
    main.next_id = 1
    yield


def test_add_note_directly():
    note = {"id": main.next_id, "title": "Лекція", "text": "Тема 5", "date": "24.05.2026 12:00"}
    main.notes.append(note)
    main.next_id += 1

    assert len(main.notes) == 1
    assert main.notes[0]["id"] == 1
    assert main.notes[0]["title"] == "Лекція"


@pytest.mark.parametrize("title, text, expected_count", [
    ("Шопінг", "Купити хліб", 1),
    ("Робота", "Написати код", 1),
    ("Спорт", "Пробіжка 5км", 1)
])
def test_parametrize_adding(title, text, expected_count):
    note = {"id": main.next_id, "title": title, "text": text, "date": "24.05.2026"}
    main.notes.append(note)
    main.next_id += 1

    assert len(main.notes) == expected_count
    assert main.notes[-1]["title"] == title


def test_invalid_id_conversion_raises_error():
    invalid_user_input = "не_число"

    with pytest.raises(ValueError):
        int(invalid_user_input)


@pytest.mark.skip(reason="Ця функція ще перебуває в розробці")
def test_cloud_sync():
    assert main.next_id == 999


@pytest.mark.xfail(reason="Відомий баг: пошук не повинен падати на пустих списках")
def test_search_expected_failure():
    assert len(main.notes) == -1

def test_broken_logic_failure():
    main.notes.append({"id": 1, "title": "Тест", "text": "Текст", "date": "24.05.2026"})
    assert len(main.notes) == 100, "Фактична кількість нотаток не дорівнює 100!"