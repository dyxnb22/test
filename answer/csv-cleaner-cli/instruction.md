# Task: csv-cleaner-cli

You need to build a Python command-line tool that cleans a dirty CSV file.

## Goal
Implement `solution/cleaner.py` so that this command works:

```bash
python solution/cleaner.py --input environment/dirty_data.csv --output solution/cleaned_data.csv
```

## Input schema
The input CSV contains these columns:

- `id`
- `name`
- `email`
- `age`
- `score`

The file may contain extra whitespace, blank lines, invalid values, and duplicate IDs.

## Cleaning rules
1. Trim leading/trailing whitespace for headers and all fields.
2. Skip fully empty rows.
3. `id` must be a positive integer. Remove rows with invalid `id`.
4. If duplicate `id` appears, keep only the first valid occurrence.
5. Normalize `name`: collapse internal whitespace to one space and convert to title case.
6. Normalize `email`: lowercase. Keep row only if email contains `@` and a `.` after `@`.
7. `age`: if valid integer in `[0, 120]`, keep it; otherwise output empty string.
8. `score`: if valid number in `[0, 100]`, output with exactly 2 decimal places; otherwise output empty string.
9. Output rows sorted by `id` ascending.
10. Output header must be exactly: `id,name,email,age,score`

## Constraints
- Use Python 3.11.
- Do not hardcode final output rows.
- The solution must be deterministic and robust.
