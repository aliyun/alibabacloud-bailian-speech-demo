[comment]: # (title and brief introduction of the sample)
## Speech Recognition of a Local Single File

English | [简体中文](./README.md)

## Java

[comment]: # (prerequisites)
### :point_right: Prerequisites

1. #### Configure Alibaba Cloud Bailian API-KEY

    Before running this example, you need to create an Alibaba Cloud account, obtain the Alibaba Cloud Bailian API-KEY, and complete necessary environment configurations. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### Configure the Workspace ID

    The qwen-audio series models are served under the workspace-specific endpoint `https://{WORKSPACE_ID}.cn-beijing.maas.aliyuncs.com`, so you **must** set:

    ```commandline
    export DASHSCOPE_WORKSPACE_ID=llm-xxxxxx
    ```

    The workspace id can be found on the Alibaba Cloud Model Studio console. Without it the example prints a hint and exits.

3. #### Java Runtime Environment

   Before running this example, you need to install Java runtime environment and Maven build tools.

[comment]: # (how to run the sample and expected results)
### :point_right: Run Example

You can run this example by executing run.sh (Linux/Mac systems) or run.bat (Windows systems).

The example program will submit files by calling the call() interface and synchronously return recognition results. The complete recognition results will be saved in the ```result.json``` file in JSON format. The full results include timestamp information at sentence and word levels.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../../docs/image/group.png" width="400"/>
