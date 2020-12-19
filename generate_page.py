#!/home/starwort/.pyenv/shims/python
import importlib
import sys

if __name__ == "__main__":
    page = sys.argv[1]
    if not sys.argv[2:]:
        sys.argv.append(f"web_pages/{page}.html")
    module = importlib.import_module("web_templates." + page)
    with open(sys.argv[2], "w") as file:
        file.write(module.generate())
