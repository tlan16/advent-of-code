import re
from pathlib import Path
from typing import Generator

input_file = Path(__file__)

valid_line_pattern = re.compile(r"^[L|R]\d+$")

def read_input() -> Generator[str]:
    with open('input.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                assert valid_line_pattern.match(line), f"Invalid line format: {line}"
                yield line

def main() -> None:
    for line in read_input():
        print(line)


if __name__ == "__main__":
    main()
