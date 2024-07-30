## 概述
通义实验室语音大模型（包括[CozyVoice](https://fun-audio-llm.github.io/)、[Paraformer](https://github.com/modelscope/FunASR)、[SenseVoice](https://fun-audio-llm.github.io/)等）可以通过阿里云百炼提供的API服务进行调用，实现<strong>语音识别</strong>（语音转文字）、<strong>语音生成</strong>（文字转语音）等功能。这些功能通过与阿里云百炼上的大语言模型API服务（包括通义千问、百川、月之暗面、零一万物、MiniMax等）结合，还可以实现<strong>语音聊天对话</strong>、<strong>语音分析理解</strong>、<strong>语音翻译</strong>等高阶AI功能。

运行本代码库中的示例代码需要调用阿里云百炼模型服务，该服务会提供一定的<strong>免费额度</strong>供开发者试用各个模型。要获得免费试用的额度并运行本代码库中的示例，开发者只需要简单的遵循以下四个步骤以满足前提条件：

1. 开通阿里云账号
1. 开通阿里云百炼模型服务
1. 创建阿里云百炼模型服务API-KEY并将其配置环境变量
1. 安装阿里云百炼SDK（DashScope SDK）

## 免费开通及配置安装步骤
1. ### 开通阿里云账号

    您需要开通阿里云账号以使用阿里云百炼模型服务。有关开通阿里云账号的操作，请参见[开通阿里云账号](https://help.aliyun.com/zh/account/user-guide/ali-cloud-account-registration-process)。

1. ### 开通阿里云百炼模型服务

    登录阿里云账号后，您还需要开通阿里云百炼模型服务。有关开通阿里云百炼模型服务的操作，请参见[开通阿里云百炼大模型服务平台](https://help.aliyun.com/zh/model-studio/getting-started/activate-alibaba-cloud-model-studio)。


1. ### 创建阿里云百炼模型服务API-KEY并将其配置环境变量
   
    阿里云百炼模型服务的所有模型均通过统一的API-KEY进行调用，您需要通过控制台创建自己的API-KEY。有关创建阿里云百炼API-KEY的的操作，请参见[API-KEY管理](https://help.aliyun.com/zh/model-studio/user-guide/api-key-management)

    通过在环境变量中配置API-KEY，您可以避免在运行示例代码时通过明文显式的指定API-KEY，从而降低API-KEY泄漏的风险。有关在环境变量中配置API-KEY的操作，请参见[通过环境变量配置API-KEY](https://help.aliyun.com/zh/model-studio/developer-reference/configure-api-key-through-environment-variables)。


1. ### 安装阿里云百炼SDK（DashScope SDK）

    #### Python

    - 前提条件

        已安装Python3.8及以上版本。请确保安装正确的Python版本，可能需要pip3 install dashscope！

    - 操作步骤

        ```bash
        pip3 install dashscope
        ```

    ### Java

    - 前提条件

        已安装JDK 1.8及以上版本。DashScope Java SDK版本请参见[Maven](https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java)。

    - 操作步骤

        执行以下命令依赖Java SDK，依赖时请将the-latest-version替换为最新版本。

        ```bash
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>dashscope-sdk-java</artifactId>
            <version>the-latest-version</version>
        </dependency>
        ```
        
        或者通过gradle依赖安装。

        ```bash
        // https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
        implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'
        ```