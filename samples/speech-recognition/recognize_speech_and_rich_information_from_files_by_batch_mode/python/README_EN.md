[comment]: # (title and brief introduction of the sample)
## Batch Audio/Video File Transcription (SDK v2 Compatibility Mode)
## Python

This example uses the DashScope SDK 2.0.2 `Client`/v2 API and the `qwen-audio-3.1-asr-flash-filetrans` model. Because the v2 batch transcription endpoint does not currently expose `sensevoice-v1`, it submits one task per URL and focuses on the file transcription flow.

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

The service transcribes each URL in a separate background task. After transcription succeeds, the example downloads the result, uses `parse_sensevoice_result` to clean the text and any returned tags, and prints it in the terminal.


[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../../docs/image/group.png" width="400"/>

