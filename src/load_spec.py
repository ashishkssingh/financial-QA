def read_api_spec() -> str:
    with open("src/api_spec.md", "r") as file:
        return file.read()
