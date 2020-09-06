
## Ref <https://github.com/sipeed/MaixPy_scripts/blob/master/multimedia/audio/play_wav.py>

from fpioa_manager import *
from Maix import I2S, GPIO
import audio,image

#Speaker I2s Initialize
fm.register(board_info.SPK_SD, fm.fpioa.GPIO0)
spk_sd=GPIO(GPIO.GPIO0, GPIO.OUT)
spk_sd.value(1)
fm.register(board_info.SPK_DIN,fm.fpioa.I2S1_OUT_D1)
fm.register(board_info.SPK_BCLK,fm.fpioa.I2S1_SCLK)
fm.register(board_info.SPK_LRCLK,fm.fpioa.I2S1_WS)
wav_dev = I2S(I2S.DEVICE_1)

#Play Wav File
def play_wav(fname):
    player = audio.Audio(path = fname)
    player.volume(100)
    wav_info = player.play_process(wav_dev)
    wav_dev.channel_config(wav_dev.CHANNEL_1,
        I2S.TRANSMITTER,resolution = I2S.RESOLUTION_16_BIT,
        align_mode = I2S.STANDARD_MODE)
    wav_dev.set_sample_rate(wav_info[1])
    while True:
        ret = player.play()
        if ret == None:
            break
        elif ret==0:
            break
    player.finish()
    print("finish")

play_wav("/sd/record_1.wav")


