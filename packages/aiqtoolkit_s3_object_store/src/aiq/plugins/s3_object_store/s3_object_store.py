# SPDX-FileCopyrightText: Copyright (c) 2024-2025, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import aioboto3

from aiq.object_store.interfaces import ObjectStore
from aiq.object_store.models import ObjectStoreItem


class S3ObjectStore(ObjectStore):

    def __init__(self,
                 bucket_name: str,
                 access_key: str | None,
                 secret_key: str | None,
                 region: str | None,
                 endpoint_url: str | None):
        self.bucket_name = bucket_name
        self.session = aioboto3.Session()
        access_key = access_key or os.environ.get("OBJECT_STORE_ACCESS_KEY")
        if not access_key:
            raise ValueError(
                "Access key is not set. Please specify it in the environment variable 'OBJECT_STORE_ACCESS_KEY_ID'.")

        secret_key = secret_key or os.environ.get("OBJECT_STORE_SECRET_KEY")
        if not secret_key:
            raise ValueError(
                "Secret key is not set. Please specify it in the environment variable 'OBJECT_STORE_SECRET_ACCESS_KEY'."
            )

        self.client_args = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "region_name": region,
            "endpoint_url": endpoint_url
        }

    async def put_object(self, key: str, data: ObjectStoreItem) -> None:
        put_args = {
            "Bucket": self.bucket_name,
            "Key": key,
            "Body": data.data,
        }
        if data.content_type:
            put_args["ContentType"] = data.content_type

        if data.metadata:
            put_args["Metadata"] = data.metadata

        async with self.session.client("s3", **self.client_args) as s3:
            await s3.put_object(**put_args)

    async def get_object(self, key: str) -> ObjectStoreItem | str:
        async with self.session.client("s3", **self.client_args) as client:
            try:
                response = await client.get_object(Bucket=self.bucket_name, Key=key)
                data = await response["Body"].read()
                return ObjectStoreItem(data=data, content_type=response['ContentType'], metadata=response['Metadata'])
            except client.exceptions.NoSuchKey:
                return f"No object found with key: {key}"

    async def delete_object(self, key: str) -> None:
        async with self.session.client("s3", **self.client_args) as s3:
            await s3.delete_object(Bucket=self.bucket_name, Key=key)
