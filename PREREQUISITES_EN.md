# Prerequisites for Running the Example Code

English | [简体中文](./PREREQUISITES.md)

## :point_right: Overview
The large audio models from Tongyi Lab (including [CosyVoice](https://fun-audio-llm.github.io/), [Paraformer](https://github.com/modelscope/FunASR), [SenseVoice](https://fun-audio-llm.github.io/), etc.) can be called via the Alibaba Cloud Model Studio API service to achieve <strong>speech recognition</strong> (speech-to-text), <strong>speech synthesis</strong> (text-to-speech), and other functions. Combined with the large language model API services on Alibaba Cloud Model Studio (including Qwen, Baichuan, Moonshot AI, 01.AI, MiniMax, etc.), these functions can further realize <strong>voice chat dialogue</strong>, <strong>voice analysis and understanding</strong>, <strong>voice translation</strong>, and other advanced AI capabilities.

To run the example code in this code repository, you need to call the Alibaba Cloud Model Studio model service, which provides a certain amount of <strong>free quota</strong> for developers to trial various models. To obtain the free trial quota and run the example code in this repository, developers only need to follow the four steps below to meet the prerequisites:

1. Open an Alibaba Cloud account
1. Activate the Alibaba Cloud Model Studio model service
1. Create an Alibaba Cloud Model Studio API-KEY and configure it as an environment variable
1. Install the Alibaba Cloud Model Studio SDK (DashScope SDK)

## :point_right: Free Activation and Configuration Installation Steps
1. ### Open an Alibaba Cloud Account

    You need to open an Alibaba Cloud account to use the Alibaba Cloud Model Studio model service. For instructions on opening an Alibaba Cloud account, see [Open an Alibaba Cloud Account](https://help.aliyun.com/zh/account/user-guide/ali-cloud-account-registration-process).

1. ### Activate the Alibaba Cloud Model Studio Model Service

    After logging in to your Alibaba Cloud account, you also need to activate the Alibaba Cloud Model Studio model service. For instructions on activating the Alibaba Cloud Model Studio model service, see [Activate Alibaba Cloud Model Studio Large Model Service Platform](https://help.aliyun.com/zh/model-studio/getting-started/activate-alibaba-cloud-model-studio).

1. ### Create an Alibaba Cloud Model Studio API-KEY and Configure It as an Environment Variable

    All models on the Alibaba Cloud Model Studio service are called using a unified API-KEY. You need to create your own API-KEY through the console. For instructions on creating an Alibaba Cloud Model Studio API-KEY, see [API-KEY Management](https://help.aliyun.com/zh/model-studio/user-guide/api-key-management).

    By configuring the API-KEY in environment variables, you can avoid specifying the API-KEY explicitly in plaintext when running example code, thereby reducing the risk of API-KEY leakage. For instructions on configuring the API-KEY via environment variables, see [Configure API-KEY Through Environment Variables](https://help.aliyun.com/zh/model-studio/developer-reference/configure-api-key-through-environment-variables).

1. ### Install the Alibaba Cloud Model Studio SDK (DashScope SDK)

    #### Python

    - Prerequisites

        Python 3.8 or higher is installed.

    - Steps

        ```bash
        pip3 install dashscope
        ```

    #### Java

    - Prerequisites

        JDK 1.8 or higher is installed. For the version of the DashScope Java SDK, see [Maven](https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java).

    - Steps

        Execute the following command to depend on the Java SDK, replacing `the-latest-version` with the latest version.

        ```bash
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>dashscope-sdk-java</artifactId>
            <version>the-latest-version</version>
        </dependency>
        ```

        Or install via Gradle.

        ```bash
        // https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
        implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'
        ```

## :point_right: Next Steps

After successfully completing the above steps, please refer to the [Application Scenarios and Development Examples](https://github.com/aliyun/alibabacloud-bailian-speech-demo#point_right-应用场景与开发示例) section to choose an example to run based on your interested application scenario.

## :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
