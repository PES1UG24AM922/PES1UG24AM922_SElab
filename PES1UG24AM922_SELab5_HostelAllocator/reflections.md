# Reflections

## 1. Security bugs can hide in code that looks fine
Before this I thought if the code runs and gives the right output, it's good enough. Bandit showed me that's not true. Things like `yaml.load`, `debug=True` and a hardcoded password all worked perfectly when I ran the program, but each one could be a real problem if someone attacked it. I didn't even know `yaml.safe_load` existed until I fixed this.

## 2. Different tools catch different things
Flake8 only cared about style like blank lines and line length. Bandit only cared about security. Pylint found things the other two missed, like the mutable default argument `preferred=[]` and unused imports. So running just one tool isn't enough, and fixing one tool's warnings doesn't mean the others are clean.

## 3. Fixing one thing can break something else
At one point my file would not even run because of a syntax error, and it took me a while to find out the real problem was earlier in the file and not on the line Pylint pointed at. It taught me to make small changes and rerun the tool after each one instead of changing everything at once.

## 4. Naming and docstrings actually matter
I used to skip docstrings and write camelCase function names out of habit. Pylint flagged almost every function for this. After renaming them to snake_case and adding short docstrings, the code was way easier to read, and my score went from around 6 to above 9. It's a small effort that makes the code easier for someone else (or me later) to understand.
