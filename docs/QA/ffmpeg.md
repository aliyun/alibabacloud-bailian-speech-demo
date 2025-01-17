# 如何安装ffmpeg

FFmpeg 是一个开源跨平台多媒体框架，用于编解码、转换、播放、录制、流式传输、分析多媒体文件。它提供了一组用于处理音频、视频和字幕的库和应用程序。在本项目的部分示例中，我们使用了ffmpeg的下述功能：
1. 流式输入流式输出的解码mp3格式音频到pcm格式。
2. 流式输入流式输出提取mp4格式视频中音轨到pcm格式音频。
3. 将mp4格式视频中音轨保存为opus格式音频文件。

## 如何在 macOS 安装 ffmpeg

可以通过homebrew直接安装

```bash
brew install ffmpeg
```

## 如何在 Windows 安装 ffmpeg

1. 下载安装包：请参考[ffmpeg官网](https://www.ffmpeg.org/download.html#build-windows) ，下载已经编译好的可执行文件。
2. 解压缩：将下载好的zip/7z文件解压缩，并且进入`bin`目录，复制`bin`目录的路径。
3. 在`设置`中搜索`编辑系统环境变量`，在`环境变量`子窗口中选择编辑用户变量`Path`，选择`新建`并将ffmpeg的bin路径复制到新建的变量中。

## 如何通过源码安装ffmpeg

在Linux系统或其他不支持直接安装ffmpeg的操作系统中，可以通过源码安装ffmpeg。
1. 下载ffmpeg源码：从[ffmpeg官网](https://www.ffmpeg.org/download.html#build-linux)下载ffmpeg源码。
2. 编译并安装:
```bash
cd ffmpeg
./configure --prefix=/usr/local/ffmpeg --enable-openssl --disable-x86asm
make && make install
```

## 检查是否安装成功

请确保成功安装ffmpeg并且将ffmpeg加入环境变量。
在终端执行`ffmpeg -version`命令，如果输出版本信息，则表示安装成功。
输出示例：
```
ffmpeg version 7.0.1 Copyright (c) 2000-2024 the FFmpeg developers
built with Apple clang version 15.0.0 (clang-1500.3.9.4)
configuration: --prefix=/opt/homebrew/Cellar/ffmpeg/7.0.1 --enable-shared --enable-pthreads --enable-version3 --cc=clang --host-cflags= --host-ldflags='-Wl,-ld_classic' --enable-ffplay --enable-gnutls --enable-gpl --enable-libaom --enable-libaribb24 --enable-libbluray --enable-libdav1d --enable-libharfbuzz --enable-libjxl --enable-libmp3lame --enable-libopus --enable-librav1e --enable-librist --enable-librubberband --enable-libsnappy --enable-libsrt --enable-libssh --enable-libsvtav1 --enable-libtesseract --enable-libtheora --enable-libvidstab --enable-libvmaf --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-libxvid --enable-lzma --enable-libfontconfig --enable-libfreetype --enable-frei0r --enable-libass --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-libspeex --enable-libsoxr --enable-libzmq --enable-libzimg --disable-libjack --disable-indev=jack --enable-videotoolbox --enable-audiotoolbox --enable-neon
libavutil      59.  8.100 / 59.  8.100
libavcodec     61.  3.100 / 61.  3.100
libavformat    61.  1.100 / 61.  1.100
libavdevice    61.  1.100 / 61.  1.100
libavfilter    10.  1.100 / 10.  1.100
libswscale      8.  1.100 /  8.  1.100
libswresample   5.  1.100 /  5.  1.100
libpostproc    58.  1.100 / 58.  1.100
```