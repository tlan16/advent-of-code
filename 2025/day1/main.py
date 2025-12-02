import re
from datetime import timedelta
from pathlib import Path
from time import perf_counter_ns
from typing import Generator, Literal
import pydantic

input_file = Path(__file__).parent / 'input.txt'
test_input_file = Path(__file__).parent / 'test_input.txt'

valid_line_pattern = re.compile(r"^[L|R]\d+$")

class Line(pydantic.BaseModel):
    direction: Literal["L", "R"]
    offset: int

    model_config = {"frozen": True}


def read_input(file: Path) -> Generator[Line]:
    with open(file, 'r') as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                assert valid_line_pattern.match(line), f"Invalid line format: {line}"
                # noinspection PyTypeChecker
                yield Line(direction=line[0], offset=int(line[1:]))

while_size = 100
def rotate(initial_position: int, line: Line) -> int:
    if line.direction == "L":
        return (initial_position - line.offset) % while_size
    else:
        return (initial_position + line.offset) % while_size


def main() -> None:
    cursor: int = 50
    counter: int = 0
    for line in read_input(input_file):
        print(f"cursor={cursor} counter={counter}")
        print(line)
        cursor = rotate(cursor, line)
        if cursor == 0:
            counter += 1
    print(f"cursor={cursor} counter={counter} [FINAL]")

if __name__ == "__main__":
    started = perf_counter_ns()
    main()
    print(f"took {timedelta(microseconds=(perf_counter_ns() - started) / 1_000)}")
