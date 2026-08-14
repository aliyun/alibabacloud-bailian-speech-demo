[comment]: # (title and brief introduction of the sample)
## Precompiled Vocabulary for Streaming Speech Recognition

English | [简体中文](./README.md)

## Python

[comment]: # (prerequisites)
### :point_right: Prerequisites

1. #### Configure the Alibaba Cloud Model Studio API-KEY

    Before running this example, you need to activate an Alibaba Cloud account, obtain the Model Studio API_KEY, and complete the required environment configuration. For detailed steps, see: [PREREQUISITES_EN.md](../../../../PREREQUISITES_EN.md)

1. #### Configure the Workspace ID

    The qwen-audio series models are served under the workspace-specific endpoint `https://{WORKSPACE_ID}.cn-beijing.maas.aliyuncs.com`, so you **must** set:

    ```commandline
    export DASHSCOPE_WORKSPACE_ID=llm-xxxxxx
    ```

    The workspace id can be found on the Alibaba Cloud Model Studio console. Without it the example prints a hint and exits.

1. #### Install Python dependencies

    The Model Studio SDK requires Python 3.8 or later. Install the dependencies of this example with:
    ```commandline
    pip3 install -r requirements.txt
    ```

[comment]: # (how to run the sample and expected results)
### :point_right: Run the Example
Run this example with:

```commandline
python3 run.py
```

The example walks through the whole vocabulary lifecycle: **create → query status → recognize by id → delete**.

```python
service = VocabularyService()
vocabulary_id = service.create_vocabulary(
    prefix='demo', target_model=MODEL, vocabulary=my_vocabulary)

# only the id is passed at recognition time, no need to resend the whole list
recognition.call(file=audio_path, phrase_id=vocabulary_id)

service.delete_vocabulary(vocabulary_id)   # always delete to free the quota
```

You can edit `my_vocabulary` in `run.py` to test your own hotwords. `weight` accepts **[1, 5]** (4 recommended) **or 50**:

> :fire: **Super hotword (weight = 50)**: **boosts recall dramatically**, for terms that must be transcribed correctly. :warning: **At most 50 of them**, and **only the Qwen-Audio-3.0-ASR-Flash-Streaming / Filetrans / Flash series support it**. In this example `通义千问` is configured as a super hotword for demonstration.

See the "Format and Weight" section of [the example overview](../README_EN.md) for the full weight table and hotword text limits.

> :warning: The vocabulary quota is limited. The example uses `try / finally` so the list is deleted even on failure; if you adapt the code, make sure the deletion path is never skipped.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../../docs/image/group.png" width="400"/>
