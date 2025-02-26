# -*- coding: utf-8 -*-

# Copyright 2021 Google LLC
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
#

import pathlib

from google.cloud import storage
from google.cloud.aiplatform import initializer
from google.cloud.aiplatform import utils

try:
    import pandas as pd
except ImportError:
    raise ImportError(
        "Pandas is not installed. Please install pandas to use VertexModel"
    )


def _serialize_dataframe(artifact_uri: str, obj: pd.DataFrame, temp_dir: str) -> str:

    """Serializes pandas DataFrame object to GCS.

    Args:
        artifact_uri (str): the GCS bucket where the serialized object will reside.
        obj (pd.DataFrame): the pandas DataFrame to serialize.
        temp_dir (str): the temporary path where this method will write a csv representation
                        of obj.

    Returns:
        The GCS path pointing to the serialized DataFrame.
    """

    # Designate csv path and write the pandas DataFrame to the path
    # Convention: file name is my_training_dataset, my_test_dataset, etc.
    path_to_csv = pathlib.Path(temp_dir) / ("my_dataset.csv")
    obj.to_csv(path_to_csv)

    gcs_bucket, gcs_blob_prefix = utils.extract_bucket_and_prefix_from_gcs_path(
        artifact_uri
    )

    local_file_name = path_to_csv.name
    blob_path = local_file_name

    if gcs_blob_prefix:
        blob_path = "/".join([gcs_blob_prefix, blob_path])

    client = storage.Client(
        project=initializer.global_config.project,
        credentials=initializer.global_config.credentials,
    )

    bucket = client.bucket(gcs_bucket)
    blob = bucket.blob(blob_path)
    blob.upload_from_filename(path_to_csv)

    gcs_path = "".join(["gs://", "/".join([blob.bucket.name, blob.name])])
    return gcs_path


def _deserialize_dataframe(artifact_uri: str) -> str:
    """Provides out-of-the-box deserialization after training and prediction is complete"""

    raise NotImplementedError
