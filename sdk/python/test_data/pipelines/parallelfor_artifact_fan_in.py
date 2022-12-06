import json
from typing import List

from kfp import dsl
from kfp.dsl import Dataset
from kfp.dsl import Input
from kfp.dsl import Output


@dsl.component
def num_to_dataset(num: int, dataset: Output[Dataset]):
    import json
    with open(dataset.path, 'w') as f:
        json.dump(num, f)


@dsl.component
def concatenate_datasets(datasets: Input[List[Dataset]],
                         concatenated_dataset: Output[Dataset]):
    import json
    values = []
    for dataset in datasets:
        with open(dataset.path) as f:
            values.append(json.load(f))
    with open(concatenated_dataset.path, 'w') as f:
        json.dump(values, f)


@dsl.component
def echo_dataset(dataset: Input[Dataset]) -> None:
    with open(dataset.path) as f:
        print(json.load(f))


@dsl.pipeline
def my_pipeline(nums: List[int] = [1, 2, 3]):
    with dsl.ParallelFor(nums) as num:
        task = num_to_dataset(num=num)
    concat_task = concatenate_datasets(
        datasets=dsl.Collected(task.outputs['dataset']))
    echo_dataset(dataset=concat_task.outputs['concatenated_dataset'])


if __name__ == '__main__':
    from kfp import compiler

    compiler.Compiler().compile(
        pipeline_func=my_pipeline,
        package_path=__file__.replace('.py', '.yaml'))
