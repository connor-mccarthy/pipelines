from typing import List

from kfp import dsl


@dsl.component
def double(num: int) -> int:
    return 2 * num


@dsl.component
def print_list_of_nums(nums: List[int]) -> None:
    print(nums)


@dsl.pipeline
def my_pipeline(nums: List[int] = [1, 2, 3]):
    with dsl.ParallelFor(nums) as num:
        task = double(num=num)
    print_list_of_nums(nums=dsl.Collected(task.output))


if __name__ == '__main__':
    from kfp import compiler

    compiler.Compiler().compile(
        pipeline_func=my_pipeline,
        package_path=__file__.replace('.py', '.yaml'))
