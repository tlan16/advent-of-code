import os
import re
from concurrent.futures import ThreadPoolExecutor
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

    def compute_invalid_id(self) -> int | None:
        total_sum = 0
        found_any = False

        for k in range(1, 10):
            multiplier = 10**k + 1
            s_min_limit = 10**(k-1)
            s_max_limit = 10**k - 1
            s_start = (self.start + multiplier - 1) // multiplier
            s_end = self.end // multiplier

            actual_start = max(s_min_limit, s_start)
            actual_end = min(s_max_limit, s_end)

            if actual_start <= actual_end:
                found_any = True
                count = actual_end - actual_start + 1
                sum_s = count * (actual_start + actual_end) // 2
                total_sum += sum_s * multiplier

        return total_sum if found_any else None


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
    result = 0
    for input in read_input(test_input_file):
        print(f"Processing input: {input}")
        input_result = input.compute_invalid_id()
        print(f"\tResult: {input_result}")
        if input_result is not None:
            result += input_result
    print(f"Final result: {result}")

def main_threaded() -> None:
    result = 0
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        started_within_thread = perf_counter_ns()
        futures = (
            executor.submit(input.compute_invalid_id)
            for input in read_input(input_file)
        )
        # Gather results as they complete
        for future in futures:
            future_result = future.result()
            if future_result is not None:
                result += future_result
        print(f"Without tread overhead took {timedelta(microseconds=(perf_counter_ns() - started_within_thread) / 1_000)}")
    print(f"Final result: {result}")

if __name__ == "__main__":
    started = perf_counter_ns()
    main_threaded()
    print(f"Overall took {timedelta(microseconds=(perf_counter_ns() - started) / 1_000)}")
