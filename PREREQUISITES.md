本文档用于说明运行阿里云百炼语音大模型SDK的前置条件.
## 服务开通
### 1. 注册阿里云账号

如果您是第一次使用百炼语音大模型产品，推荐使用阿里云账号开通服务。更多创建阿里云账号操作，请参见[准备阿里云账号](https://help.aliyun.com/zh/account/user-guide/ali-cloud-account-registration-process)。

### 2. 开通百炼语音大模型服务

    - 登录阿里云账号，访问大模型服务平台[百炼控制台](https://bailian.console.aliyun.com/)。
   ![](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1272235171/p798709.png)

    - 在模型广场/应用广场界面，点击**去开通**按钮，即可开通模型调用服务。

    - 更多模型开通信息请查看[百炼大模型服务产品](https://help.aliyun.com/document_detail/2586399.html)。


### 3. 获取API\_KEY
   - 在百炼控制台界面右上角头像位置，鼠标悬浮后，展示API-KEY，点击后进入API-KEY管理页面。
![](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0049794171/p796772.png)

   - 点击【创建新的API-KEY】，会自动创建一条属于这个账号的API-KEY。列表上展示API-KEY密文，点击【查看】可以看到API-KEY的明文信息。
   ![](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4090250171/p779690.png)

   - 更多API\_KEY 信息请访问[获取文档](https://help.aliyun.com/document_detail/2712195.html)。

## 环境配置
API_KEY是访问阿里云为访问大模型服务推出的全新认证机制。您可以使用配置环境变量的方法，避免在调用百炼服务的SDK时显式地配置API-KEY，从而降低泄漏风险。
以下是将API_KEY配置为环境变量的说明。

### Linux

当您使用Linux系统（如Ubuntu、CentOS等）中的命令行添加DashScope的API-KEY为环境变量时，可以选择在当前会话添加临时性环境变量，或对当前用户添加永久性环境变量。

- 添加临时性环境变量

如果您仅想在当前会话中添加并使用临时性环境变量，您可以运行以下命令：

 ```bash
 # 用您的 DashScope API-KEY 代替 YOUR_DASHSCOPE_API_KEY
export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
 ```

您可以在当前会话运行以下命令检查环境变量是否生效：

 ```bash
 echo $DASHSCOPE_API_KEY
 ```

- 对当前用户添加永久性环境变量

如果您想对当前用户添加永久性环境变量，使得在该用户的新会话中也可以使用该环境变量，您可以把以下命令语句复制并添加到~/.bashrc文件中：

 ```bash
 # 用您的 DashScope API-KEY 代替 YOUR_DASHSCOPE_API_KEY
export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
 ```

或直接运行以下命令将上述命令语句添加到~/.bashrc中：
 ```bash
 # 用您的 DashScope API-KEY 代替 YOUR_DASHSCOPE_API_KEY
echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.bashrc

 ```

添加完成后，您可以运行以下命令使得环境变量生效：
```bash
source ~/.bashrc
```

您可以新建立一个会话，运行以下命令检查环境变量是否生效：
```bash
echo $DASHSCOPE_API_KEY
```

### MacOS

当您使用MacOS系统中的命令行添加DashScope的API-KEY为环境变量时，可以选择在当前会话添加临时性环境变量，或对当前用户添加永久性环境变量。

- 添加临时性环境变量
如果您仅想在当前会话中添加并使用临时性环境变量，您可以运行以下命令：
 ```bash
 # 用您的 DashScope API-KEY 代替 YOUR_DASHSCOPE_API_KEY
export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
 ```

您可以在当前会话运行以下命令检查环境变量是否生效：
 ```bash
 echo $DASHSCOPE_API_KEY
 ```

- 对当前用户添加永久性环境变量

如果您想对当前用户添加永久性环境变量，使得在该用户的新会话中也可以使用该环境变量，您可以根据您使用的Shell类型把以下命令复制并添加到~/.zshrc或~/.bash_profile文件中。

 ```bash
 # 用您的 DashScope API-KEY 代替 YOUR_DASHSCOPE_API_KEY
export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY
```
或直接运行以下命令将上述命令语句添加到~/.zshrc或~/.bash_profile中：
 ```bash
## 如果您的Shell类型是Zsh，运行以下命令
echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.zshrc

## 如果您的Shell类型是Bash，运行以下命令
echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.bash_profile
```

添加完成后，您可以运行以下命令使得环境变量生效：
```bash
# 如果您的Shell类型是Zsh，运行以下命令
source ~/.zshrc

# 如果您的Shell类型是Bash，运行以下命令
source ~/.bash_profile
```
您可以新建立一个会话，运行以下命令检查环境变量是否生效：
```bash
echo $DASHSCOPE_API_KEY
```

### Windows

在Windows系统中，您可以使用CMD或PowerShell（推荐）运行命令。

- 添加临时性环境变量

如果您仅想在当前会话中添加并使用临时性环境变量，您可以运行以下命令：

```bash
# 用您的 DashScope API-KEY 代替 YOUR_DASHSCOPE_API_KEY
set DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
```

您可以在当前会话运行以下命令检查环境变量是否生效：

```bash
echo %DASHSCOPE_API_KEY%
```

- 对当前用户添加永久性环境变量

如果您想对当前用户添加永久性环境变量，使得在该用户的新会话中也可以使用该环境变量，您可以把以下命令语句复制并添加到“环境变量”中：

```bash
# 用您的 DashScope API-KEY 代替 YOUR_DASHSCOPE_API_KEY
setx DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
```

添加完成后，您可以运行以下命令使得环境变量生效：
```bash
echo %DASHSCOPE_API_KEY%
```

### 使用PyCharm IDE
如果您使用PyCharm 等IDE进行开发及运行，由于运行机制的不同，您在环境变量中的配置可能无法正确访问。以下提供两种推荐方案。

- 方案一：在IDE中添加环境变量
```
点击菜单栏中的 Run -> Edit Configurations...
点击左侧选中需要运行的项目，并在右侧菜单中配置 Environment Variables
添加：DASHSCOPE_API_KEY=YOUR_DASHSCOPE_API_KEY
```

- 方案二：通过.env文件配置环境变量
```
点击菜单栏中的 Run -> Edit Configurations...
点击左侧选中需要运行的项目，并在右侧菜单中选择 Path to '.env' Files 导入您的.env文件
您可以在文件中添加：DASHSCOPE_API_KEY=YOUR_DASHSCOPE_API_KEY
```


## SDK安装

### python

- 前提条件

已安装Python3.8及以上版本。请确保安装正确的Python版本，可能需要pip3 install dashscope！

- 操作步骤

```bash
pip3 install dashscope
```

### java

- 前提条件

已安装JDK1.8及以上版本。SDK版本请参见[Maven](https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java)。

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