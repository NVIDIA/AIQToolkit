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

from abc import ABC
from abc import abstractmethod

from .models import ObjectStoreItem


class ObjectStore(ABC):
    """
    Abstract interface for a key-value store.
    """

    @abstractmethod
    async def put_object(self, key: str, data: ObjectStoreItem) -> None:
        """
        Save a value in the key-value store and return a unique key.
        """
        pass

    @abstractmethod
    async def get_object(self, key: str) -> ObjectStoreItem | str:
        """
        Get a value from the key-value store by key.
        """
        pass

    @abstractmethod
    async def delete_object(self, key: str) -> None:
        """
        Delete a value from the key-value store by key.
        """
        pass
