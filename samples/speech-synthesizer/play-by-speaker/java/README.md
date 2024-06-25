## 前提条件
本示例依赖百炼SDK，MP3编解码和播放使用了jLayer。您可以按照下方的说明导入依赖。

### 安装 mp3编解码和播放库 java 依赖

- jLayer
```
//pom.xml 通过maven导入依赖
        <!-- https://mvnrepository.com/artifact/javazoom/jlayer -->
        <dependency>
            <groupId>javazoom</groupId>
            <artifactId>jlayer</artifactId>
            <version>1.0.1</version>
        </dependency>
```

### 百炼SDK
```
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>dashscope-sdk-java</artifactId>
    <version>the-latest-version</version>
</dependency>
```