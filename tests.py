from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

# print("Result for current directory:")
# print(get_files_info("calculator", "."))

# print("Result for 'pkg' directory:")
# print(get_files_info("calculator", "pkg"))

# print("Result for '/bin' directory:")
# print(get_files_info("calculator", "/bin"))

# print("Result for '../' directory:")
# print(get_files_info("calculator", "../"))

# print("Result for 'lorem.txt' file:")
# print(get_file_content("calculator", "lorem.txt"))

print("Result for 'main.py' file:")
print(get_file_content("calculator", "main.py"))

print("Result for 'calculator.py' file:")
print(get_file_content("calculator", "pkg/calculator.py"))

print("Result for '/bin/cat' file:")
print(get_file_content("calculator", "/bin/cat"))

print("Result for 'does_not_exist.py' file:")
print(get_file_content("calculator", "pkg/does_not_exist.py"))