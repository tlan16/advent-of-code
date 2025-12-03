from datetime import timedelta
from functools import lru_cache
from pathlib import Path
from time import perf_counter_ns
from typing import Generator, Literal
import pydantic

input_file = Path(__file__).parent / 'input.txt'
assert input_file.is_file()
test_input_file = Path(__file__).parent / 'test_input.txt'
assert test_input_file.is_file()

class Line(pydantic.BaseModel):
    direction: Literal["L", "R"]
    offset: int = pydantic.Field(gt=0)

    model_config = {"frozen": True}


def read_input(file: Path) -> Generator[Line]:
    with open(file, 'r') as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                # noinspection PyTypeChecker
                yield Line(direction=line[0], offset=line[1:])

while_size = 100


@lru_cache
def calculate_distance_to_zero(positon: int, line: Line) -> int:
    if line.direction == "R":
        return (while_size - positon) % while_size or while_size
    else:
        return positon or while_size

@lru_cache
def calculate_passed_zero_times(positon: int, line: Line) -> int:
    distance_to_zero = calculate_distance_to_zero(positon, line)

    if line.offset < distance_to_zero:
        return 0
    return 1 + (line.offset - distance_to_zero) // while_size

@lru_cache
def rotate(initial_position: int, line: Line) -> tuple[int, int]:
    if line.direction == "L":
        new_position = (initial_position - line.offset) % while_size
    else:
        new_position = (initial_position + line.offset) % while_size

    passed_zero_times = calculate_passed_zero_times(initial_position, line)
    print(f"cursor as {initial_position}, rotating {line.direction} {line.offset}. New position: {new_position}. Passed zero times: {passed_zero_times}")
    return new_position, passed_zero_times


def main() -> None:
    cursor: int = 50
    passed_zero_times: int = 0
    for line in read_input(input_file):
        cursor, passed_zero_times_per_iter = rotate(cursor, line)
        passed_zero_times += passed_zero_times_per_iter
    print(f"cursor={cursor} passed_zero_times={passed_zero_times} [FINAL]")


if __name__ == "__main__":
    started = perf_counter_ns()
    main()
    print(f"took {timedelta(microseconds=(perf_counter_ns() - started) / 1_000)}")
