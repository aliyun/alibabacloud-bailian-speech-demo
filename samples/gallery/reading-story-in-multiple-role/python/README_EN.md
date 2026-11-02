## Role-Based Story Reading

English | [简体中文](./README.md)

This example uses the DashScope SDK 2.0.2 `Client`/v2 API and Qwen-Audio-3.1-TTS to narrate a complete story by role. It is suitable for audiobooks, online education, and similar scenarios.
<!--
### :point_right: Applicable Scenarios

| Application Scenario | Typical Usage | Usage Instructions                |
|--------------|--------|---------------------|
 -->


## Python

### :point_right: Prerequisites

1. #### Configure Alibaba Cloud API-KEY

    Before running this example, you need to activate an Alibaba Cloud account, obtain the API-KEY, and perform necessary environment configurations. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

1. #### Install Python Dependencies

    The Alibaba Cloud SDK requires Python 3.8 or higher. You can install the dependencies for this example using the following command:
    ```commandline
    pip3 install -r requirements.txt
    ```

### :point_right: Run Example

```commandline
python3 run.py
```

The `qwen-audio-3.1-tts-flash` model narrates "Duck Mother," "Duck Baby," and "Narrator" with the verified `longanfengyue_v3.1` voice. The code keeps a separate voice variable for each role so you can replace them with other voices available to your account. The story content is stored in `story.json`.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../../docs/image/group.png" width="400"/>