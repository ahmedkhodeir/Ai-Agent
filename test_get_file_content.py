from functions.get_file_content import get_file_content

print("--- Testing lorem truncation ---")
content = get_file_content("calculator", "lorem.txt")
print("Length:", len(content))
print("Ends with truncate message?:", content.endswith('truncated at 10000 characters]'))
print()

print("--- Testing reading main.py ---")
print(get_file_content("calculator", "main.py"))
print()

print("--- Testing reading pkg/calculator.py ---")
print(get_file_content("calculator", "pkg/calculator.py"))
print()

print("--- Testing reading /bin/cat (should error) ---")
print(get_file_content("calculator", "/bin/cat"))
print()

print("--- Testing nonexistent file ---")
print(get_file_content("calculator", "pkg/does_not_exist.py"))
print()
