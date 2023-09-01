# Copyright 2023 The Kubeflow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Dict, List

from google_cloud_pipeline_components import _image
from google_cloud_pipeline_components import _placeholders
from kfp.dsl import ConcatPlaceholder
from kfp.dsl import container_component
from kfp.dsl import ContainerSpec
from kfp.dsl import OutputPath


@container_component
def dataproc_create_spark_sql_batch(
    gcp_resources: OutputPath(str),
    location: str = 'us-central1',
    batch_id: str = '',
    labels: Dict[str, str] = {},
    container_image: str = '',
    runtime_config_version: str = '',
    runtime_config_properties: Dict[str, str] = {},
    service_account: str = '',
    network_tags: List[str] = [],
    kms_key: str = '',
    network_uri: str = '',
    subnetwork_uri: str = '',
    metastore_service: str = '',
    spark_history_dataproc_cluster: str = '',
    query_file_uri: str = '',
    query_variables: Dict[str, str] = {},
    jar_file_uris: List[str] = [],
    project: str = _placeholders.PROJECT_ID_PLACEHOLDER,
):
  # fmt: off
  """Create a Dataproc Spark SQL batch workload and wait for it to finish.

  Args:
      location: Location of the Dataproc batch workload. If
        not set, defaults to `"us-central1"`.
      batch_id: The ID to use for the batch, which will become
        the final component of the batch's resource name. If none is
        specified, a default name will be generated by the component.  This
        value must be 4-63 characters. Valid characters are /[a-z][0-9]-/.
      labels: The labels to associate with this batch. Label
        keys must contain 1 to 63 characters, and must conform to RFC 1035.
        Label values may be empty, but, if present, must contain 1 to 63
        characters, and must conform to RFC 1035. No more than 32 labels can
        be associated with a batch.  An object containing a list of `"key":
        value` pairs.
          Example: `{ "name": "wrench", "mass": "1.3kg", "count": "3" }`.
      container_image: Optional custom container image for the
        job runtime environment. If not specified, a default container image
        will be used.
      runtime_config_version: Version of the batch runtime.
      runtime_config_properties: Runtime configuration for the workload.
      service_account: Service account that is used to execute the workload.
      network_tags: Tags used for network traffic control.
      kms_key: The Cloud KMS key to use for encryption.
      network_uri: Network URI to connect workload to.
      subnetwork_uri: Subnetwork URI to connect workload to.
      metastore_service: Resource name of an existing Dataproc Metastore
        service.
      spark_history_dataproc_cluster: The Spark History Server configuration for
        the workload.
      query_file_uri: The HCFS URI of the script that contains Spark SQL queries
        to execute.
      query_variables: Mapping of query variable names to values (equivalent to
        the Spark SQL command: `SET name="value";`). An object containing a
        list of `"key": value` pairs.
          Example: `{ "name": "wrench", "mass": "1.3kg", "count": "3" }`.
      jar_file_uris: HCFS URIs of jar files to be added to the Spark
        `CLASSPATH`.
      project: Project to run the Dataproc batch workload. Defaults to the project in which the PipelineJob is run.

  Returns:
      gcp_resources: Serialized gcp_resources proto tracking the Dataproc batch workload. For more details, see
          https://github.com/kubeflow/pipelines/blob/master/components/google-cloud/google_cloud_pipeline_components/proto/README.md.
  """
  # fmt: on
  return ContainerSpec(
      image=_image.GCPC_IMAGE_TAG,
      command=[
          'python3',
          '-u',
          '-m',
          'google_cloud_pipeline_components.container.v1.dataproc.create_spark_sql_batch.launcher',
      ],
      args=[
          '--type',
          'DataprocSparkSqlBatch',
          '--payload',
          ConcatPlaceholder([
              '{',
              '"labels": ',
              labels,
              ', "runtime_config": {',
              '"version": "',
              runtime_config_version,
              '"',
              ', "container_image": "',
              container_image,
              '"',
              ', "properties": ',
              runtime_config_properties,
              '}',
              ', "environment_config": {',
              '"execution_config": {',
              '"service_account": "',
              service_account,
              '"',
              ', "network_tags": ',
              network_tags,
              ', "kms_key": "',
              kms_key,
              '"',
              ', "network_uri": "',
              network_uri,
              '"',
              ', "subnetwork_uri": "',
              subnetwork_uri,
              '"',
              '}',
              ', "peripherals_config": {',
              '"metastore_service": "',
              metastore_service,
              '"',
              ', "spark_history_server_config": { ',
              '"dataproc_cluster": "',
              spark_history_dataproc_cluster,
              '"',
              '}',
              '}',
              '}',
              ', "spark_sql_batch": {',
              '"query_file_uri": "',
              query_file_uri,
              '"',
              ', "query_variables": ',
              query_variables,
              ', "jar_file_uris": ',
              jar_file_uris,
              '}',
              '}',
          ]),
          '--project',
          project,
          '--location',
          location,
          '--batch_id',
          batch_id,
          '--gcp_resources',
          gcp_resources,
      ],
  )
