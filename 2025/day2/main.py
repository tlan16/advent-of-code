import re
from datetime import timedelta
from pathlib import Path
from time import perf_counter_ns
from typing import Generator, Literal
import pydantic

input_file = Path(__file__).parent / 'input.txt'
assert input_file.is_file()
test_input_file = Path(__file__).parent / 'test_input.txt'
assert test_input_file.is_file()

class Input(pydantic.BaseModel):
    start: int = pydantic.Field(gt=0)
    end: int = pydantic.Field(gt=0)

    model_config = {"frozen": True}


def read_input(file: Path) -> Generator[Input]:
    with open(file, 'r') as file:
        for line in file:
            ranges = line.strip().split(",")
            for range in ranges:
                range_parts = range.strip().split("-")
                if len(range_parts) == 2:
                    # noinspection PyTypeChecker
                    yield Input(start=range_parts[0], end=range_parts[1])

def main() -> None:
    for input in read_input(test_input_file):
        print(input)

if __name__ == "__main__":
    started = perf_counter_ns()
    main()
    print(f"took {timedelta(microseconds=(perf_counter_ns() - started) / 1_000)}")
