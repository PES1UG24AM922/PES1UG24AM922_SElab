# hostel_allocation.py: Lint & Security Issues

## Flake8

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| E302 | Style | 20, 30, 54, 62, 70, 74, 78, 85, 92, 96, 102 | Expected 2 blank lines before function, found 1 | Add a second blank line before each top-level `def` |
| E305 | Style | 116 | Expected 2 blank lines after function, found 1 | Add a second blank line before `if __name__ == "__main__":` |
| E501 | Style | 26 | Line too long (92 > 79) | Split the room dict into one key per line |
| E501 | Style | 89 | Line too long (83 > 79) | Wrap the `ValueError` message onto its own line |
| E501 | Style | 100 | Line too long (82 > 79) | Move escaped value into a `details` variable before the f-string |

## Bandit

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| B506 | Security (Medium) | 21 | Unsafe `yaml.load` can build arbitrary objects | Use `yaml.safe_load(text)` |
| B311 | Security (Low) | 56 | `random` is not cryptographically secure | Use `secrets.SystemRandom().sample(...)` |
| B106 | Security (Low) | 66 | Hardcoded DB password | Read from `WARDEN_DB_PASSWORD` env variable |
| B612 | Security (Medium) | 72 | Insecure `logging.config.listen` | Replace with local `logging.basicConfig(...)` |
| B201 | Security (High) | 80 | Flask `debug=True` exposes Werkzeug debugger | Use `app.run(debug=False)` |

## Pylint

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| C0301 | Convention | 98 | Line too long (116/100) | Split the call across lines |
| C0114 | Convention | 1 | Missing module docstring | Add a module docstring |
| C0116 | Convention | Most functions | Missing function docstring | Add a one-line docstring to each function |
| C0103 | Convention | Most functions | camelCase names, not snake_case | Rename (e.g. `loadConfig` to `load_config`) |
| W0102 | Warning | 29 | Mutable default `preferred=[]` | Use `preferred=None`, then set `[]` inside |
| C0123 | Convention | 30 | `type()` used for type check | Use `isinstance(year, int)` |
| W0613 | Warning | 29 | Unused argument `gender` | Use it to match room gender |
| C0206 | Convention | 60 | Dict iteration without `.items()` | Iterate `rooms.values()` |
| W0611 | Warning | 2, 4 | Unused imports `sys`, `logging` | Remove them |
| C0303 | Convention | 37, 48, 52, 116 | Trailing whitespace | Strip trailing spaces |
| C0305 | Convention | 124 | Trailing newlines at end of file | Keep a single newline at EOF |
