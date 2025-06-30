import json
from datetime import date
from pathlib import Path
from typing import List, Dict

DATA_FILE = Path(__file__).resolve().parent.parent / "routines.json"


def load_data() -> Dict[str, List[Dict]]:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_data(data: Dict[str, List[Dict]]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_task(task_date: str, time: str, description: str) -> None:
    data = load_data()
    tasks = data.setdefault(task_date, [])
    tasks.append({"time": time, "description": description, "done": False})
    save_data(data)


def complete_task(task_date: str, index: int) -> None:
    data = load_data()
    tasks = data.get(task_date)
    if not tasks or index < 0 or index >= len(tasks):
        raise IndexError("Task not found")
    tasks[index]["done"] = True
    save_data(data)


def list_tasks(task_date: str) -> List[Dict]:
    data = load_data()
    return data.get(task_date, [])


def list_today() -> List[Dict]:
    return list_tasks(date.today().isoformat())


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Daily Routine CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_p = subparsers.add_parser("add", help="Add a task")
    add_p.add_argument("date", help="YYYY-MM-DD")
    add_p.add_argument("time", help="HH:MM")
    add_p.add_argument("description", help="Task description")

    done_p = subparsers.add_parser("done", help="Mark a task as done")
    done_p.add_argument("date", help="YYYY-MM-DD")
    done_p.add_argument("index", type=int, help="Task index starting at 0")

    list_p = subparsers.add_parser("list", help="List tasks for a date")
    list_p.add_argument("date", nargs="?", default=date.today().isoformat())

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.date, args.time, args.description)
    elif args.command == "done":
        try:
            complete_task(args.date, args.index)
        except IndexError:
            print("Task not found")
    elif args.command == "list":
        tasks = list_tasks(args.date)
        for i, t in enumerate(tasks):
            status = "[x]" if t.get("done") else "[ ]"
            print(f"{i}. {status} {t['time']} - {t['description']}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
