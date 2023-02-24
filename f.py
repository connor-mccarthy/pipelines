from kfp import dsl
from kfp.components import pipeline_task


def foo_platform_set_bar_feature(task: pipeline_task.PipelineTask,
                                 val: str) -> pipeline_task.PipelineTask:
    platform_key = 'platform_foo'
    feature_key = 'bar'

    platform_struct = task.platform_config.get(platform_key, {})
    platform_struct[feature_key] = val
    task.platform_config[platform_key] = platform_struct
    return task


def foo_platform_append_bop_feature(task: pipeline_task.PipelineTask,
                                    val: str) -> pipeline_task.PipelineTask:
    platform_key = 'platform_foo'
    feature_key = 'bop'

    platform_struct = task.platform_config.get(platform_key, {})
    feature_list = platform_struct.get(feature_key, [])
    feature_list.append(val)
    platform_struct[feature_key] = feature_list
    task.platform_config[platform_key] = platform_struct
    return task


def baz_platform_set_bat_feature(task: pipeline_task.PipelineTask,
                                 val: str) -> pipeline_task.PipelineTask:
    platform_key = 'platform_baz'
    feature_key = 'bat'

    platform_struct = task.platform_config.get(platform_key, {})
    platform_struct[feature_key] = val
    task.platform_config[platform_key] = platform_struct
    return task


@dsl.component
def comp():
    pass


@dsl.pipeline
def my_pipeline():
    task = comp()
    foo_platform_set_bar_feature(task, 12)
    foo_platform_append_bop_feature(task, 'element')
    baz_platform_set_bat_feature(task, 'hello')


if __name__ == '__main__':
    import warnings

    from kfp import compiler

    warnings.filterwarnings('ignore')
    ir_file = __file__.replace('.py', '.yaml')
    compiler.Compiler().compile(pipeline_func=my_pipeline, package_path=ir_file)

from kfp import components

loaded = components.load_component_from_file(ir_file)
print(loaded.platform_spec)


@dsl.pipeline
def outer():
    task = comp()
    x = loaded()
    # # should raise! but doesn't
    # baz_platform_set_bat_feature(x, 'y')
    # should be present, but isn't
    baz_platform_set_bat_feature(task, 'y')


# from pprint import pprint

# pprint(loaded.platform_spec)
# pprint(my_pipeline.platform_spec)
# # need a merge step here
# pprint(my_pipeline.platform_spec)
