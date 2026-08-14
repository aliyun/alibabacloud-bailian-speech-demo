[comment]: # (title and brief introduction of the sample)
## Conversation Context for Streaming Speech Recognition

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

    > :warning: **The context (`raw_input`) requires dashscope >= 1.25.23.** On older versions `raw_input` is silently ignored by the SDK, so the context is never sent to the service — recognition still returns normally but the context has no effect. Verify with `pip3 show dashscope`.

[comment]: # (how to run the sample and expected results)
### :point_right: Run the Example
Run this example with:

```commandline
python3 run.py
```

The example runs 4 scenarios in sequence. Each one first prints the number of context messages actually sent, then streams the recognition result:

| Scenario | Description |
| --- | --- |
| 1. Without context | Baseline for comparison |
| 2. Dialog history | Two complete user / assistant turns |
| 3. Domain word list | A single `user` message carrying 6 domain terms |
| 4. Trimming | 7 user messages and an oversized text on purpose, to show automatic trimming |

The context is passed through the `raw_input` parameter:

```python
input_context = {
    'context': [
        {'role': 'user',      'content': [{'type': 'input_text', 'text': '你好啊'}]},
        {'role': 'assistant', 'content': [{'type': 'text',       'text': '你好啊，我是通义千问。'}]},
    ]
}
recognition.start(raw_input=input_context)   # can also be passed to recognition.call()
```

You can edit `dialog_history` and `domain_terms` in `run.py` to test your own context. `build_context()` automatically trims the message count and text length according to the service constraints.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../../docs/image/group.png" width="400"/>
