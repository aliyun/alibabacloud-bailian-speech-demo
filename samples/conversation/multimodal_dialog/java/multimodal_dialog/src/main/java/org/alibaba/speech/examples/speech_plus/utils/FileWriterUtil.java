package org.alibaba.speech.examples.speech_plus.utils;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;

/**
 * 文件写入工具类。
 * 支持创建文件、开始写入数据、追加写入数据和结束写入操作。
 * 使用 ByteBuffer 存储数据并将数据写入指定的文件中。
 */
public class FileWriterUtil {

    private File file;
    private FileOutputStream fos;
    private FileChannel fc;

    /**
     * 创建一个新的文件。
     *
     * @param filePath 文件路径
     */
    public void createFile(String filePath) throws IOException {
        file = new File(filePath);
        if (!file.exists()) {
            file.createNewFile();
        }

        fos = new FileOutputStream(file, true);
        fc = fos.getChannel();
    }

    /**
     * 写入数据。
     *
     * @param data 要追加的数据
     */
    public void Writing(ByteBuffer data) throws IOException {
        fc.position(fc.size());
        fc.write(data);
    }

    /**
     * 结束写入操作。
     */
    public void finishWriting() throws IOException {
        if (fc != null) {
            fc.close();
        }

        if (fos != null) {
            fos.close();
        }
    }
}