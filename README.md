# Daily Routine Application

This is a simple command-line application for managing daily routines.

## Usage

Install dependencies (none required) and run the script using Python 3:

```bash
python routine_app/daily_routine.py [command] [options]
```

### Commands

- `add <date> <time> <description>`: Add a task for the specified date.
- `done <date> <index>`: Mark the task at the given index as done.
- `list [date]`: List tasks for the given date (defaults to today).
- `export <date> <file>`: Export tasks for the date to a CSV file.

Data is stored in `routines.json` in the project root.
Exported CSV files can be imported into spreadsheet applications like Google Sheets.
