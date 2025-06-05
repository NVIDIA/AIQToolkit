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

from aiq.builder.builder import Builder
from aiq.cli.register_workflow import register_object_store
from aiq.data_models.object_store import ObjectStoreBaseConfig

from .interfaces import ObjectStore
from .models import ObjectStoreItem


class MemObjectStoreConfig(ObjectStoreBaseConfig, name="memory"):
    pass


class MemObjectStore(ObjectStore):

    def __init__(self) -> None:
        self._store: dict[str, ObjectStoreItem] = {}

    async def put_object(
        self,
        key: str,
        data: ObjectStoreItem,
    ) -> None:
        self._store[key] = data
        return

    async def get_object(self, key: str) -> ObjectStoreItem | str:
        return self._store.get(key, f"No object found with key: {key}")

    async def delete_object(self, key: str) -> None:
        self._store.pop(key, None)
        return


@register_object_store(config_type=MemObjectStoreConfig)
async def mem_object_store(config: MemObjectStoreConfig, builder: Builder):
    yield MemObjectStore()
