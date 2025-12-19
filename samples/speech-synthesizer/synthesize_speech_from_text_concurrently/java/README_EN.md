## Concurrent Speech Synthesis Invocation

English | [简体中文](./README.md)

## Java

### :point_right: Prerequisites

1. #### Configure Alibaba Cloud API-KEY

    Before running this example, you need to create an Alibaba Cloud account, obtain the API-KEY, and complete environment configuration. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### Java Runtime Environment

   Before running this example, you need to install Java runtime environment and Maven build tool.

### :point_right: How to Run the Example

You can run this example by executing run.sh (for Linux/Mac systems) or run.bat (for Windows systems).

When running the example, it will concurrently synthesize "欢迎体验阿里云百炼大模型语音合成服务！" using the longanhuan voice style and save it to the `<requestId>.mp3` file.

In the Java concurrent example, three types of resource pools are used: connection pool, object pool, and thread pool. Reusing objects and connections can effectively reduce the time cost of establishing connections.

You can modify the `task_list` to add/remove tasks for synthesizing specified number of texts. Use the `peakThreadNum` parameter to modify the maximum number of threads. It is recommended not to exceed the number of CPU cores on the machine. Use the `runTimes` parameter to set the number of task executions.

:information_source: **Note**: Personal account appkeys currently only support 3 concurrency. Contact us if you need to enable higher concurrency.

### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
