from functions.run_python_file import run_python_file

print("--- Run main.py (no args) ---")
print(run_python_file("calculator", "main.py"))
print()

print("--- Run main.py with args ---")
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print()

print("--- Run tests.py ---")
print(run_python_file("calculator", "tests.py"))
print()

print("--- Attempt path traversal ---")
print(run_python_file("calculator", "../main.py"))
print()

print("--- Nonexistent file ---")
print(run_python_file("calculator", "nonexistent.py"))
print()

print("--- Non-python file ---")
print(run_python_file("calculator", "lorem.txt"))
print()
