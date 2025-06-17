## Concurrent Speech Synthesis Invocation

English | [简体中文](./README.md)

## Python

### :point_right: Prerequisites

1. #### Configure Alibaba Cloud API-KEY

    Before running this example, you need to create an Alibaba Cloud account, obtain the API-KEY, and complete environment configuration. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

1. #### Install Python dependencies

    The Alibaba Cloud SDK requires Python 3.8 or higher. You can use the following command to install dependencies for this example:
    ```commandline
    pip3 install -r requirements.txt
    ```

### :point_right: How to Run the Example
You can use the following command to run this example:

```commandline
python3 run.py
```

When running the example, it will concurrently synthesize "I am XXX, welcome to experience Alibaba Cloud Qwen large model speech synthesis service!" using three different voice styles and save them to results/result_v<voice_style>_p<thread_id>.mp3 files.

You can modify the task_list to add/remove tasks for synthesizing specified number of texts. Use the processes parameter in multiprocessing.Pool to modify the maximum number of processes. It is recommended not to exceed the number of CPU cores on the machine.

In the Python example, due to Python's Global Interpreter Lock (GIL), multiprocessing is used to achieve concurrency.

:information_source: **Note**: Personal account appkeys currently only support 3 concurrency. Contact us if you need to enable higher concurrency.


[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>