import datetime
import json
import os

notes = []
next_id = 1


def load_notes():
    global notes, next_id
    if os.path.exists("notes.json"):
        try:
            with open("notes.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                notes = data.get("notes", [])
                next_id = data.get("next_id", 1)
        except Exception:
            notes = []
            next_id = 1


def save_notes():
    try:
        with open("notes.json", "w", encoding="utf-8") as file:
            json.dump({"notes": notes, "next_id": next_id}, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"\n[СИСТЕМНА ПОМИЛКА]: Не вдалося зберегти дані у файл: {e}")


def show_menu():
    print()
    print("=" * 40)
    print("        НОТАТНИК - ГОЛОВНЕ МЕНЮ")
    print("=" * 40)
    print("  1. Додати нотатку")
    print("  2. Переглянути всі нотатки")
    print("  3. Пошук нотаток")
    print("  4. Редагувати нотатку")
    print("  5. Видалити нотатку")
    print("  0. Вийти")
    print("=" * 40)


def show_success(msg):
    print(f"\n[УСПІХ] {msg}")


def show_error(msg):
    print(f"\n[ПОМИЛКА] {msg}")


def add_note():
    global next_id
    print("\n--- Додати нотатку ---")
    title = input("Заголовок: ").strip()
    text = input("Текст: ").strip()

    if not title:
        show_error("Заголовок не може бути порожнім!")
        return
    if not text:
        show_error("Текст нотатки не може бути порожнім!")
        return

    date_str = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    note = {
        "id": next_id,
        "title": title,
        "text": text,
        "date": date_str,
    }
    notes.append(note)
    next_id += 1

    save_notes()
    show_success(f"Нотатку '{title}' додано успішно!")


def search_notes():
    print("\n--- Пошук нотаток ---")
    if not notes:
        show_error("Нотаток немає.")
        return
    query = input("Введіть пошуковий запит: ").strip().lower()

    if not query:
        show_error("Пошуковий запит не може бути порожнім!")
        return

    results = [n for n in notes if query in n["title"].lower() or query in n["text"].lower()]

    if results:
        print(f"\nЗнайдено {len(results)} нотатку(ок):")
        for n in results:
            print(f"  [{n['id']}] {n['title']} ({n['date']})")
            print(f"  Текст: {n['text']}\n  " + "-" * 36)
    else:
        show_error("Нічого не знайдено.")


def view_notes():
    print("\n--- Всі нотатки ---")
    if not notes:
        show_error("Список нотаток порожній.")
        return

    print("Оберіть сортування:")
    print("  1. За порядком створення (старі -> нові)")
    print("  2. За алфавітом заголовків (А-Я)")
    print("  3. Від найновіших до найстаріших")
    sort_choice = input("Ваш вибір сортування (за замовчуванням - 1): ").strip()

    if sort_choice == "2":
        display_notes = sorted(notes, key=lambda x: x["title"].lower())
    elif sort_choice == "3":
        display_notes = sorted(notes, key=lambda x: x["id"], reverse=True)
    else:
        display_notes = notes

    for n in display_notes:
        print(f"\n  ID: {n['id']}  |  {n['title']}  |  {n['date']}")
        print(f"  {n['text']}")
        print("  " + "-" * 36)


def edit_note():
    print("\n--- Редагувати нотатку ---")
    if not notes:
        show_error("Немає нотаток для редагування.")
        return
    try:
        nid = int(
            input("Введіть ID нотатки для редагування: "))
    except ValueError:
        show_error("ID має бути числом!")
        return

    for n in notes:
        if n["id"] == nid:
            print(f"Поточний заголовок: {n['title']}")
            new_title = input("Новий заголовок (Enter - залишити): ").strip()
            print(f"Поточний текст: {n['text']}")
            new_text = input("Новий текст (Enter - залишити): ").strip()

            if new_title:
                n["title"] = new_title
            if new_text:
                n["text"] = new_text

            if not n["title"] or not n["text"]:
                show_error("Редагування скасовано! Заголовок або текст не можуть стати порожніми.")
                load_notes()
                return

            save_notes()
            show_success("Нотатку оновлено!")
            return
    show_error(f"Нотатку з ID {nid} не знайдено.")


def delete_note():
    print("\n--- Видалити нотатку ---")
    if not notes:
        show_error("Немає нотаток для видалення.")
        return

    nid_input = input("Введіть ID нотатки для видалення: ").strip()

    try:
        nid = int(nid_input)
    except ValueError:
        show_error("ID має бути цілим числом!")
        return

    for i, n in enumerate(notes):
        if n["id"] == nid:
            notes.pop(i)
            save_notes()
            show_success(f"Нотатку ID {nid} видалено.")
            return
    show_error(f"Нотатку з ID {nid} не знайдено.")


def main():
    load_notes()
    print("Ласкаво просимо до Нотатника!")
    while True:
        show_menu()
        choice = input("Ваш вибір: ").strip()
        if choice == "1":
            add_note()
        elif choice == "2":
            view_notes()
        elif choice == "3":
            search_notes()
        elif choice == "4":
            edit_note()
        elif choice == "5":
            delete_note()
        elif choice == "0":
            print("До побачення!")
            break
        else:
            show_error("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
