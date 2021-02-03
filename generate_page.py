#!/home/starwort/.pyenv/shims/python
import importlib
import sys


def main(in_module: str, out_file: str = None) -> None:
    if out_file is None:
        out_file = f"docs/{in_module}.html"
    module = importlib.import_module("web_templates." + in_module)
    with open(out_file, "w") as file:
        file.write(module.generate())


if __name__ == "__main__":
    main(*sys.argv[1:3])
