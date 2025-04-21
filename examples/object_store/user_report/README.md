<!--
SPDX-FileCopyrightText: Copyright (c) 2025, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Report Tool

AgentIQ tool that makes use of an Object Store to retrieve data.

## Installation and Setup
If you have not already done so, follow the instructions in the [Install Guide](../../docs/source/intro/install.md) to create the development environment and install AgentIQ.

### Install this Workflow:

From the root directory of the AgentIQ library, run the following commands:

```bash
uv pip install -e examples/report
```

### Setting up MinIO (Optional)
If you want to run this example in a local setup without creating a bucket in AWS, you can set up MinIO in your local machine. MinIO is an object storage system and acts as drop-in replacement for AWS S3.

For the up-to-date installation instructions of MinIO, see [MinIO Page](https://github.com/minio/minio) and MinIO client see [MinIO Client Page](https://github.com/minio/mc)

#### MacOS
```
brew install minio/stable/mc
mc --help
mc alias set myminio http://localhost:9000 minioadmin minioadmin

brew install minio/stable/minio
minio server ~/.minio
```

#### Linux
```
curl https://dl.min.io/client/mc/release/linux-amd64/mc \
  --create-dirs \
  -o $HOME/minio-binaries/mc

chmod +x $HOME/minio-binaries/mc
export PATH=$PATH:$HOME/minio-binaries/
mc --help
mc alias set myminio http://localhost:9000 minioadmin minioadmin

wget https://dl.min.io/server/minio/release/linux-amd64/archive/minio_20250422221226.0.0_amd64.deb -O minio.deb
sudo dpkg -i minio.deb
minio server ~/.minio
```

### Load Mock Data
To load mock data to minIO, use the `upload_to_minio.sh` script in this directory. For this example, we will load the mock user reports in the `data/object_store` directory.

```
./upload_to_minio.sh data/object_store myminio my-bucket
```

## Run the Workflow

Run the following command from the root of the AgentIQ repo to execute this workflow with the specified input:

### Example 1
```
aiq run --config_file examples/object_store/user_report/configs/config.yml --input "Give me the latest report of user 67890"
```

**Expected Output**
```console
aiq run --config_file examples/object_store/user_report/configs/config.yml --input "Give me the latest report of user 67890"
2025-04-23 17:30:04,742 - aiq.cli.commands.start - INFO - Starting AgentIQ from config file: 'examples/object_store/user_report/configs/config.yml'
2025-04-23 17:30:04,745 - aiq.cli.commands.start - WARNING - The front end type in the config file (fastapi) does not match the command name (console). Overwriting the config file front end.
2025-04-23 17:30:04,782 - aiq.profiler.decorators.framework_wrapper - INFO - Langchain callback handler registered
2025-04-23 17:30:05,404 - aiq.agent.react_agent.agent - INFO - Filling the prompt variables "tools" and "tool_names", using the tools provided in the config.
2025-04-23 17:30:05,404 - aiq.agent.react_agent.agent - INFO - Adding the tools' input schema to the tools' description
2025-04-23 17:30:05,405 - aiq.agent.react_agent.agent - INFO - Initialized ReAct Agent Graph
2025-04-23 17:30:05,410 - aiq.agent.react_agent.agent - INFO - ReAct Graph built and compiled successfully

Configuration Summary:
--------------------
Workflow Type: react_agent
Number of Functions: 1
Number of LLMs: 1
Number of Embedders: 0
Number of Memory: 0
Number of Retrievers: 0

2025-04-23 17:30:05,411 - aiq.front_ends.console.console_front_end_plugin - INFO - Processing input: ('Give me the latest report of user 67890',)
2025-04-23 17:30:05,414 - aiq.agent.react_agent.agent - INFO - Querying agent, attempt: 1
2025-04-23 17:30:05,975 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-04-23 17:30:06,327 - aiq.agent.react_agent.agent - INFO - The user's question was: Give me the latest report of user 67890
2025-04-23 17:30:06,327 - aiq.agent.react_agent.agent - INFO - The agent's thoughts are:
Question: Give me the latest report of user 67890
Thought: I need to fetch the latest report for user 67890.
Action: user_report
Action Input: {"user_id": "67890", "date": null}
2025-04-23 17:30:06,331 - aiq.agent.react_agent.agent - INFO - Calling tool user_report with input: {"user_id": "67890", "date": null}
2025-04-23 17:30:06,331 - aiq.agent.react_agent.agent - INFO - Successfully parsed structured tool input from Action Input
2025-04-23 17:30:06,332 - aiq_report.register - INFO - Fetching report from /reports/67890/latest.json
2025-04-23 17:30:06,476 - aiq.agent.react_agent.agent - INFO - Querying agent, attempt: 1
2025-04-23 17:30:06,779 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-04-23 17:30:07,900 - aiq.agent.react_agent.agent - INFO - 

The agent's thoughts are:
Thought: I now have the latest report for user 67890.
Final Answer: The latest report for user 67890 is as follows:

- Timestamp: 2025-04-21T15:40:00Z
- System:
  - OS: macOS 14.1
  - CPU Usage: 43%
  - Memory Usage: 8.1 GB / 16 GB
  - Disk Space: 230 GB free of 512 GB
- Network:
  - Latency: 95 ms
  - Packet Loss: 0%
  - VPN Connected: True
- Errors: None
- Recommendations: 
  - System operating normally
  - No action required
2025-04-23 17:30:07,904 - aiq.observability.async_otel_listener - INFO - Intermediate step stream completed. No more events will arrive.
2025-04-23 17:30:07,905 - aiq.front_ends.console.console_front_end_plugin - INFO - --------------------------------------------------
Workflow Result:
['The latest report for user 67890 is as follows:\n\n- Timestamp: 2025-04-21T15:40:00Z\n- System:\n  - OS: macOS 14.1\n  - CPU Usage: 43%\n  - Memory Usage: 8.1 GB / 16 GB\n  - Disk Space: 230 GB free of 512 GB\n- Network:\n  - Latency: 95 ms\n  - Packet Loss: 0%\n  - VPN Connected: True\n- Errors: None\n- Recommendations: \n  - System operating normally\n  - No action required']
```

### Example 2
```
aiq run --config_file examples/object_store/user_report/configs/config.yml --input "Give me the latest report of user 12345 on April 15th 2025"
```

**Expected Output**
```console
aiq run --config_file examples/object_store/user_report/configs/config.yml --input "Give me the latest report of user 12345 on April 15th 2025"
2025-04-23 17:35:27,582 - aiq.cli.commands.start - INFO - Starting AgentIQ from config file: 'examples/object_store/user_report/configs/config.yml'
2025-04-23 17:35:27,585 - aiq.cli.commands.start - WARNING - The front end type in the config file (fastapi) does not match the command name (console). Overwriting the config file front end.
2025-04-23 17:35:27,625 - aiq.profiler.decorators.framework_wrapper - INFO - Langchain callback handler registered
2025-04-23 17:35:28,214 - aiq.agent.react_agent.agent - INFO - Filling the prompt variables "tools" and "tool_names", using the tools provided in the config.
2025-04-23 17:35:28,214 - aiq.agent.react_agent.agent - INFO - Adding the tools' input schema to the tools' description
2025-04-23 17:35:28,214 - aiq.agent.react_agent.agent - INFO - Initialized ReAct Agent Graph
2025-04-23 17:35:28,219 - aiq.agent.react_agent.agent - INFO - ReAct Graph built and compiled successfully

Configuration Summary:
--------------------
Workflow Type: react_agent
Number of Functions: 1
Number of LLMs: 1
Number of Embedders: 0
Number of Memory: 0
Number of Retrievers: 0

2025-04-23 17:35:28,221 - aiq.front_ends.console.console_front_end_plugin - INFO - Processing input: ('Give me the latest report of user 12345 on April 15th 2025',)
2025-04-23 17:35:28,223 - aiq.agent.react_agent.agent - INFO - Querying agent, attempt: 1
2025-04-23 17:35:28,709 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-04-23 17:35:29,455 - aiq.agent.react_agent.agent - INFO - The user's question was: Give me the latest report of user 12345 on April 15th 2025
2025-04-23 17:35:29,455 - aiq.agent.react_agent.agent - INFO - The agent's thoughts are:
Thought: I need to fetch the user diagnostic report for user ID 12345 on April 15th, 2025.
Action: user_report
Action Input: {"user_id": "12345", "date": "2025-04-15"}
2025-04-23 17:35:29,460 - aiq.agent.react_agent.agent - INFO - Calling tool user_report with input: {"user_id": "12345", "date": "2025-04-15"}
2025-04-23 17:35:29,460 - aiq.agent.react_agent.agent - INFO - Successfully parsed structured tool input from Action Input
2025-04-23 17:35:29,462 - aiq_report.register - INFO - Fetching report from /reports/12345/2025-04-15.json
2025-04-23 17:35:29,625 - aiq.agent.react_agent.agent - INFO - Querying agent, attempt: 1
2025-04-23 17:35:29,902 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-04-23 17:35:31,596 - aiq.agent.react_agent.agent - INFO - 

The agent's thoughts are:
Thought: I have obtained the latest report for user 12345 on April 15th, 2025.
Final Answer: The latest report for user 12345 on April 15th, 2025, is as follows:

- **System Information:**
  - Operating System: Windows 11
  - CPU Usage: 82%
  - Memory Usage: 6.3 GB / 8 GB
  - Disk Space: 120 GB free of 500 GB

- **Network Information:**
  - Latency: 240 ms
  - Packet Loss: 0.5%
  - VPN Connected: False

- **Errors:**
  - Timestamp: 2025-04-15T10:21:59Z
  - Message: "App crash detected: 'PhotoEditorPro.exe' exited unexpectedly"
  - Severity: High

- **Recommendations:**
  - Update graphics driver
  - Check for overheating hardware
  - Enable automatic crash reporting
2025-04-23 17:35:31,600 - aiq.observability.async_otel_listener - INFO - Intermediate step stream completed. No more events will arrive.
2025-04-23 17:35:31,601 - aiq.front_ends.console.console_front_end_plugin - INFO - --------------------------------------------------
Workflow Result:
['The latest report for user 12345 on April 15th, 2025, is as follows:\n\n- **System Information:**\n  - Operating System: Windows 11\n  - CPU Usage: 82%\n  - Memory Usage: 6.3 GB / 8 GB\n  - Disk Space: 120 GB free of 500 GB\n\n- **Network Information:**\n  - Latency: 240 ms\n  - Packet Loss: 0.5%\n  - VPN Connected: False\n\n- **Errors:**\n  - Timestamp: 2025-04-15T10:21:59Z\n  - Message: "App crash detected: \'PhotoEditorPro.exe\' exited unexpectedly"\n  - Severity: High\n\n- **Recommendations:**\n  - Update graphics driver\n  - Check for overheating hardware\n  - Enable automatic crash reporting']
```


### Example 3
```
aiq run --config_file examples/object_store/user_report/configs/config.yml --input 'Create a latest report for user 6789 with the following JSON contents:
    {
        "recommendations": [
            "Update graphics driver",
            "Check for overheating hardware",
            "Enable automatic crash reporting"
        ]
    }
'
```

**Expected Output**
```console
aiq run --config_file examples/object_store/user_report/configs/config.yml --input 'Create a latest report for user 6789 with the following JSON contents:
    {
        "recommendations": [
            "Update graphics driver",
            "Check for overheating hardware",
            "Enable automatic crash reporting"
        ]
    }
'
2025-04-24 09:57:16,849 - aiq.cli.commands.start - INFO - Starting AgentIQ from config file: 'examples/object_store/user_report/configs/config.yml'
2025-04-24 09:57:16,873 - aiq.cli.commands.start - WARNING - The front end type in the config file (fastapi) does not match the command name (console). Overwriting the config file front end.
2025-04-24 09:57:16,950 - aiq.profiler.decorators.framework_wrapper - INFO - Langchain callback handler registered
2025-04-24 09:57:17,574 - aiq.agent.react_agent.agent - INFO - Filling the prompt variables "tools" and "tool_names", using the tools provided in the config.
2025-04-24 09:57:17,574 - aiq.agent.react_agent.agent - INFO - Adding the tools' input schema to the tools' description
2025-04-24 09:57:17,574 - aiq.agent.react_agent.agent - INFO - Initialized ReAct Agent Graph
2025-04-24 09:57:17,579 - aiq.agent.react_agent.agent - INFO - ReAct Graph built and compiled successfully

Configuration Summary:
--------------------
Workflow Type: react_agent
Number of Functions: 2
Number of LLMs: 1
Number of Embedders: 0
Number of Memory: 0
Number of Object Stores: 1
Number of Retrievers: 0

2025-04-24 09:57:17,580 - aiq.front_ends.console.console_front_end_plugin - INFO - Processing input: ('Create a latest report for user 6789 with the following JSON contents:\n    {\n        "recommendations": [\n            "Update graphics driver",\n            "Check for overheating hardware",\n            "Enable automatic crash reporting"\n        ]\n    }\n',)
2025-04-24 09:57:17,583 - aiq.agent.react_agent.agent - INFO - Querying agent, attempt: 1
2025-04-24 09:57:18,109 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-04-24 09:57:18,968 - aiq.agent.react_agent.agent - INFO - The user's question was: Create a latest report for user 6789 with the following JSON contents:
    {
        "recommendations": [
            "Update graphics driver",
            "Check for overheating hardware",
            "Enable automatic crash reporting"
        ]
    }

2025-04-24 09:57:18,969 - aiq.agent.react_agent.agent - INFO - The agent's thoughts are:
Thought: I need to use the `put_user_report` tool to create a latest report for user 6789 with the provided JSON contents.
Action: put_user_report
Action Input: {"report": "{\"recommendations\": [\"Update graphics driver\", \"Check for overheating hardware\", \"Enable automatic crash reporting\"]}", "user_id": "6789", "date": null}
2025-04-24 09:57:18,972 - aiq.agent.react_agent.agent - INFO - Calling tool put_user_report with input: {"report": "{\"recommendations\": [\"Update graphics driver\", \"Check for overheating hardware\", \"Enable automatic crash reporting\"]}", "user_id": "6789", "date": null}
2025-04-24 09:57:18,972 - aiq.agent.react_agent.agent - INFO - Successfully parsed structured tool input from Action Input
2025-04-24 09:57:18,974 - aiq_report.register - INFO - Fetching report from /reports/6789/latest.json
2025-04-24 09:57:19,153 - aiq.agent.react_agent.agent - INFO - Querying agent, attempt: 1
2025-04-24 09:57:19,566 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-04-24 09:57:20,102 - aiq.agent.react_agent.agent - INFO - 

The agent's thoughts are:
Thought: The empty response indicates that the report was successfully created for user 6789. 

Final Answer: The latest report for user 6789 has been successfully created with the specified recommendations.
2025-04-24 09:57:20,106 - aiq.observability.async_otel_listener - INFO - Intermediate step stream completed. No more events will arrive.
2025-04-24 09:57:20,106 - aiq.front_ends.console.console_front_end_plugin - INFO - --------------------------------------------------
Workflow Result:
['The latest report for user 6789 has been successfully created with the specified recommendations.']
--------------------------------------------------
```

### Example 4 (Continued from Example 3)
```
aiq run --config_file examples/object_store/user_report/configs/config.yml --input 'Get the latest report for user 6789'
```

**Expected Output**
```console
aiq run --config_file examples/object_store/user_report/configs/config.yml --input 'Get the latest report for user 6789'
2025-04-24 10:00:08,498 - aiq.cli.commands.start - INFO - Starting AgentIQ from config file: 'examples/object_store/user_report/configs/config.yml'
2025-04-24 10:00:08,504 - aiq.cli.commands.start - WARNING - The front end type in the config file (fastapi) does not match the command name (console). Overwriting the config file front end.
2025-04-24 10:00:08,556 - aiq.profiler.decorators.framework_wrapper - INFO - Langchain callback handler registered
2025-04-24 10:00:12,666 - aiq.agent.react_agent.agent - INFO - Filling the prompt variables "tools" and "tool_names", using the tools provided in the config.
2025-04-24 10:00:12,666 - aiq.agent.react_agent.agent - INFO - Adding the tools' input schema to the tools' description
2025-04-24 10:00:12,666 - aiq.agent.react_agent.agent - INFO - Initialized ReAct Agent Graph
2025-04-24 10:00:12,675 - aiq.agent.react_agent.agent - INFO - ReAct Graph built and compiled successfully

Configuration Summary:
--------------------
Workflow Type: react_agent
Number of Functions: 2
Number of LLMs: 1
Number of Embedders: 0
Number of Memory: 0
Number of Object Stores: 1
Number of Retrievers: 0

2025-04-24 10:00:12,676 - aiq.front_ends.console.console_front_end_plugin - INFO - Processing input: ('Get the latest report for user 6789',)
2025-04-24 10:00:12,680 - aiq.agent.react_agent.agent - INFO - Querying agent, attempt: 1
2025-04-24 10:00:13,344 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-04-24 10:00:13,796 - aiq.agent.react_agent.agent - INFO - The user's question was: Get the latest report for user 6789
2025-04-24 10:00:13,797 - aiq.agent.react_agent.agent - INFO - The agent's thoughts are:
Thought: I need to fetch the latest report for user 6789.
Action: get_user_report
Action Input: {"user_id": "6789", "date": null}
2025-04-24 10:00:13,803 - aiq.agent.react_agent.agent - INFO - Calling tool get_user_report with input: {"user_id": "6789", "date": null}
2025-04-24 10:00:13,803 - aiq.agent.react_agent.agent - INFO - Successfully parsed structured tool input from Action Input
2025-04-24 10:00:13,806 - aiq_report.register - INFO - Fetching report from /reports/6789/latest.json
2025-04-24 10:00:14,116 - aiq.agent.react_agent.agent - INFO - Querying agent, attempt: 1
2025-04-24 10:00:14,911 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-04-24 10:00:15,371 - aiq.agent.react_agent.agent - INFO - 

The agent's thoughts are:
Thought: I have obtained the latest report for user 6789.
Final Answer: The latest report for user 6789 includes the following recommendations:
1. Update graphics driver
2. Check for overheating hardware
3. Enable automatic crash reporting
2025-04-24 10:00:15,374 - aiq.observability.async_otel_listener - INFO - Intermediate step stream completed. No more events will arrive.
2025-04-24 10:00:15,375 - aiq.front_ends.console.console_front_end_plugin - INFO - --------------------------------------------------
Workflow Result:
['The latest report for user 6789 includes the following recommendations:\n1. Update graphics driver\n2. Check for overheating hardware\n3. Enable automatic crash reporting']
```