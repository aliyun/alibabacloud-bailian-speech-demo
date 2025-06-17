[comment]: # (title and brief introduction of the sample)
## Batch Audio/Video File Rich Text Speech Recognition
## Python

[comment]: # (prerequisites)
### :point_right: Prerequisites

1. #### Configure Alibaba Cloud Bailian API-KEY

    Before running this example, you need to create an Alibaba Cloud account, obtain the Alibaba Cloud Bailian API-KEY, and complete necessary environment configurations. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### Install Python Dependencies

    The Alibaba Cloud Bailian SDK requires Python 3.8 or higher. You can install the dependencies for this example using the following command:
    ```commandline
    pip3 install -r requirements.txt
    ```

[comment]: # (how to run the sample and expected results)
### :point_right: Run Example
You can run this example using the following command:

```commandline
python3 run.py
```

When running the example, the audio file recognition service will process the submitted file list in the background. After successful transcription, each file's recognition results will be parsed and printed in the terminal using the parse_sensevoice_result tool.


[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>

