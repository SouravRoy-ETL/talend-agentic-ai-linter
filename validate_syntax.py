import os
import py_compile
import re

has_errors = False
syntax_errors = []

for root, _, files in os.walk("src"):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                py_compile.compile(path, doraise=True)
            except py_compile.PyCompileError as e:
                error_msg = str(e)
                match = re.search(r"line (\d+)", error_msg)
                lineno = match.group(1) if match else "?"
                first_line = error_msg.strip().splitlines()[-1]
                syntax_errors.append((path, lineno, first_line))
                has_errors = True

if has_errors:
    print("\033[91mSyntax errors found:\033[0m")
    for file, lineno, msg in syntax_errors:
        print(f"\033[93m - {file}, line {lineno}: {msg}\033[0m")
else:
    print("\033[92mNo syntax errors found.\033[0m")
