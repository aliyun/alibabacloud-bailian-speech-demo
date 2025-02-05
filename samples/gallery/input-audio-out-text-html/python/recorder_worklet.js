class PCMProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
        this.port.onmessage = (event) => {
            if (event.data === 'stop') {
                this.port.postMessage('prepare to stop');
                this.isStopped = true;
                if (this.buffer.length > 0) {
                    this.port.postMessage(new Int16Array(this.buffer));  // 发送剩余的样本
                    this.port.postMessage({'event':'stopped'});
                    this.buffer = [];  // 清空缓冲区
                }
            }
        };
        this.buffer = [];  // 初始化缓冲区来存储采样点
        this.targetSampleCount = 1600;  // 目标样本数量100ms
    }

    process(inputs, outputs, parameters) {
        const input = inputs[0];
        if (input.length > 0) {
            // 获取输入缓冲区的第一个通道
            const inputData = input[0];

            // 将Float32Array转换为Int16Array，并积累到缓冲区
            for (let i = 0; i < inputData.length; i++) {
                const sample = Math.max(-32768, Math.min(32767, Math.round(inputData[i] * 32767)));
                this.buffer.push(sample);
            }

            // 当缓冲区里的样本数量达到目标值时，发送给主线程
            while (this.buffer.length >= this.targetSampleCount) {
                // 从缓冲区中取出目标数量的样本
                const pcmData = this.buffer.splice(0, this.targetSampleCount);
                this.port.postMessage(new Int16Array(pcmData));  // 将选定的样本发送到主线程
                this.port.postMessage({'event':'sending'});
            }
        }

        return true;  // 继续处理
    }
}

registerProcessor('pcm-processor', PCMProcessor);
