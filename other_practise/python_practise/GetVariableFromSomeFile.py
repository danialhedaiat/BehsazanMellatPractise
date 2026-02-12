import ast


def get_variable(file_path, variable_name):
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()

    code = ast.parse(data)

    for node in code.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == variable_name:
                    return ast.literal_eval(node.value)

    return KeyError(f"Variable '{variable_name}' not found in {file_path}")

result = get_variable("SomeFile", "my_dict")
print(result)

