# Copyright 2023 The Kubeflow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict, List, Optional, Union

from google.protobuf import json_format
from google.protobuf import message
from kfp import dsl
from kfp.dsl import PipelineTask
from kfp.kubernetes import common
from kfp.kubernetes import kubernetes_executor_config_pb2 as pb


@dsl.container_component
def CreatePVC(
    name: dsl.OutputPath(str),
    access_modes: List[str],
    size: str,
    pvc_name: Optional[str] = None,
    pvc_name_suffix: Optional[str] = None,
    storage_class_name: Optional[str] = '',
    volume_name: Optional[str] = None,
    annotations: Optional[Dict[str, str]] = None,
):
    """Create a PersistentVolumeClaim, which can be used by downstream tasks.
    See `PersistentVolume.

    <https://kubernetes.io/docs/concepts/storage/persistent-
    volumes/#persistent-volumes>`_ and `PersistentVolumeClaim
    <https://kubernetes.io/docs/concepts/storage/persistent-
    volumes/#persistentvolumeclaims>`_ documentation for more information about
    the component input parameters.

    Args:
        access_modes: AccessModes to request for the provisioned PVC. May
            be multiple of ReadWriteOnce, ReadOnlyMany, ReadWriteMany, or
            ReadWriteOncePod.
        size: The size of storage requested by the PVC that will be provisioned.
        pvc_name: Name of the PVC. Only one of pvc_name and pvc_name_suffix can
            be provided.
        pvc_name_suffix: Prefix to use for a dynamically generated name, which
            will take the form <argo-workflow-name>-<pvc_name_suffix>. Only one
            of pvc_name and pvc_name_suffix can be provided.
        storage_class_name: Name of StorageClass from which to provision the PV
            to back the PVC. `None` indicates to use the cluster's default
            storage_class_name. Set to `''` for a statically specified PVC.
        volume_name: Pre-existing PersistentVolume that should back the
            provisioned PersistentVolumeClaim. Used for statically
            specified PV only.
        annotations: Annotations for the PVC's metadata.

    Outputs:
        name: The name of the generated PVC.
    """

    return dsl.ContainerSpec(image='argostub/createpvc')


def mount_pvc(
    task: PipelineTask,
    pvc_name: str,
    mount_path: str,
) -> PipelineTask:
    """Mount a PersistentVolumeClaim to the task container.

    Args:
        task: Pipeline task.
        pvc_name: Name of the PVC to mount. Can also be a runtime-generated name
            reference provided by ```kubernetes.CreatePvcOp().outputs['name']```.
        mount_path: Path to which the PVC should be mounted as a volume.
    """

    msg = common.get_existing_kubernetes_config_as_message(task)

    pvc_mount = pb.PvcMount(mount_path=mount_path)
    _assign_pvc_name_to_msg(pvc_mount, pvc_name)

    msg.pvc_mount.append(pvc_mount)
    task.platform_config['kubernetes'] = json_format.MessageToDict(msg)

    return task


@dsl.container_component
def DeletePVC(pvc_name: str):
    """Delete a PersistentVolumeClaim.

    Args:
        pvc_name: Name of the PVC to delete. Can also be a runtime-generated name
            reference provided by `kubernetes.CreatePvcOp().outputs['name']`.
    """
    return dsl.ContainerSpec(image='argostub/deletepvc')


def _assign_pvc_name_to_msg(msg: message.Message,
                            pvc_name: Union[str, 'PipelineChannel']) -> None:
    if isinstance(pvc_name, str):
        msg.constant = pvc_name
    elif hasattr(pvc_name, 'task_name'):
        if pvc_name.task_name is None:
            msg.component_input_parameter = pvc_name.name
        else:
            msg.task_output_parameter.producer_task = pvc_name.task_name
            msg.task_output_parameter.output_parameter_key = pvc_name.name
    else:
        raise ValueError(
            f'Argument for {"pvc_name"!r} must be an instance of str or PipelineChannel. Got unknown input type: {type(pvc_name)!r}. '
        )
