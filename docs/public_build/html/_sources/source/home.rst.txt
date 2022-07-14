KFP SDK API Reference Documentation
===================================
This website contains the KFP SDK API Reference Documentation for the Kubeflow Pipelines SDK `kfp`. For complete Kubeflow Pipelines project documentation, visit `kubeflow.org <https://kubeflow.org/>`_.

What is Kubeflow Pipelines?
---------------------------
Kubeflow Pipelines is a platform for building and deploying portable, scalable machine learning workflows based on Docker containers within the `Kubeflow <https://www.kubeflow.org/>`_ project.

Use Kubeflow Pipelines to compose a multi-step workflow `pipeline <https://www.kubeflow.org/docs/components/pipelines/concepts/pipeline/>`_ as a `graph <https://www.kubeflow.org/docs/components/pipelines/concepts/graph/>`_ of containerized `tasks <https://www.kubeflow.org/docs/components/pipelines/concepts/step/>`_ using Python code and/or YAML. Then, `run <https://www.kubeflow.org/docs/components/pipelines/concepts/run/>`_ your pipeline with specified pipeline arguments, rerun your pipeline with new arguments or data, `schedule <https://www.kubeflow.org/docs/components/pipelines/concepts/run-trigger/>`_ your pipeline to run on a recurring basis, organize your runs into `experiments <https://www.kubeflow.org/docs/components/pipelines/concepts/experiment/>`_, save machine learning artifacts to compliant `artifact registries <https://www.kubeflow.org/docs/components/pipelines/concepts/metadata/>`_, and visualize it all through the `Kubeflow Dashboard <https://www.kubeflow.org/docs/components/central-dash/overview/>`_.


Installation
--------------------------
To install the `kfp` pre-release, run:
::

   pip install kfp --pre


Getting started
--------------------------
The following is an example that uses Python code to author a simple pipeline:

.. literalinclude:: source/getting_started_pipeline.py
