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

from typing import Optional

from pydantic import Field

from aiq.builder.builder import Builder
from aiq.cli.register_workflow import register_telemetry_exporter
from aiq.data_models.telemetry_exporter import TelemetryExporterBaseConfig


class WeaveTelemetryExporter(TelemetryExporterBaseConfig, name="weave"):
    """A telemetry exporter to transmit traces to Weights & Biases Weave using OpenTelemetry."""
    project: str = Field(description="The W&B project name.")
    entity: Optional[str] = Field(default=None, description="The W&B username or team name.")


@register_telemetry_exporter(config_type=WeaveTelemetryExporter)
async def weave_telemetry_exporter(config: WeaveTelemetryExporter, builder: Builder):
    import weave

    if config.entity:
        _ = weave.init(project_name=f"{config.entity}/{config.project}")
    else:
        _ = weave.init(project_name=config.project)

    class NoOpSpanExporter:

        def export(self, spans):
            return None

        def shutdown(self):
            return None

    # just yielding None errors with 'NoneType' object has no attribute 'export'
    yield NoOpSpanExporter()
