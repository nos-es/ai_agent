from functions.get_file_content import get_file_content


result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt: {result}")
print(f"lorem.txt truncated: {'truncated' in result}")
result = get_file_content("calculator", "main.py")
print(f"main.py: {result}")
print(f"main.py truncated: {'truncated' in result}")
result = get_file_content("calculator", "pkg/calculator.py")
print(f"pkg/calculator: {result}")
print(f"pkg calculator truncated: {'truncated' in result}")
result = get_file_content("calculator", "/bin/cat")
print(f"/bin/cat: {result}")
print(f"/bin/cat truncated: {'truncated' in result}")
result = get_file_content("calculator", "pkg/does_not_exist.py")
print(f"pkg/does_not_exist.py: {result}")
print(f"pkg/does_not_exist truncated: {'truncated' in result}")
