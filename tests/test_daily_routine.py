import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import routine_app.daily_routine as dr


def setup_function(function):
    # Backup existing data file
    if dr.DATA_FILE.exists():
        os.rename(dr.DATA_FILE, dr.DATA_FILE.with_suffix(".bak"))
    dr.DATA_FILE.write_text("{}", encoding="utf-8")


def teardown_function(function):
    if dr.DATA_FILE.exists():
        dr.DATA_FILE.unlink()
    bak = dr.DATA_FILE.with_suffix(".bak")
    if bak.exists():
        os.rename(bak, dr.DATA_FILE)


def test_add_and_list(tmp_path):
    dr.DATA_FILE = tmp_path / "routines.json"
    dr.add_task("2024-01-01", "08:00", "Test Task")
    tasks = dr.list_tasks("2024-01-01")
    assert len(tasks) == 1
    assert tasks[0]["description"] == "Test Task"
    assert not tasks[0]["done"]


def test_complete_task(tmp_path):
    dr.DATA_FILE = tmp_path / "routines.json"
    dr.add_task("2024-01-01", "09:00", "Another Task")
    dr.complete_task("2024-01-01", 0)
    tasks = dr.list_tasks("2024-01-01")
    assert tasks[0]["done"]
