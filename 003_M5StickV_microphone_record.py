
## Ref <https://github.com/sipeed/MaixPy_scripts/blob/master/multimedia/audio/record_wav.py>


from Maix import GPIO, I2S, FFT
import image,lcd,math,time,gc,lcd
from board import board_info
from fpioa_manager import fm
import audio

lcd.init()
lcd.clear()
lcd.rotation(2)

sample_rate = 22050
sample_points = 4096

# I2S MIC GPIO
fm.register(board_info.MIC_LRCLK, fm.fpioa.I2S0_WS, force=True)
fm.register(board_info.MIC_DAT, fm.fpioa.I2S0_IN_D0, force=True)
fm.register(board_info.MIC_CLK, fm.fpioa.I2S0_SCLK, force=True)

mic_dev = I2S(I2S.DEVICE_0)
mic_dev.channel_config(mic_dev.CHANNEL_0, mic_dev.RECEIVER, align_mode=I2S.STANDARD_MODE)
mic_dev.set_sample_rate(sample_rate)
print(mic_dev)


def record_wav(fname):
    player = audio.Audio(path=fname, is_create=True, samplerate=sample_rate)
    queue = []
    for i in range(100):
        tmp = mic_dev.record(sample_points)
        if len(queue) > 0:
            ret = player.record(queue[0])
            queue.pop(0)
        lcd.draw_string(20,50,"REC",i)
        mic_dev.wait_record()
        queue.append(tmp)
    player.finish()

lcd.draw_string(20,50,"REC")
record_wav("/sd/record_1.wav")
lcd.draw_string(20,50,"finish")

