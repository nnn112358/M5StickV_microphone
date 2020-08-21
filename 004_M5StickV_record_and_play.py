## M5StickV Mic Record and Speaker Play
## A button is Play
## B button is Record

from Maix import GPIO, I2S, FFT
import image,lcd,math,time,gc,lcd
from board import board_info
from fpioa_manager import *
import audio

# Button
fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
fm.register(board_info.BUTTON_B, fm.fpioa.GPIO2)
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)
but_b = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)

#Microphone I2S Initialize

sample_rate = 22050
sample_points = 4096

fm.register(board_info.MIC_LRCLK, fm.fpioa.I2S0_WS, force=True)
fm.register(board_info.MIC_DAT, fm.fpioa.I2S0_IN_D0, force=True)
fm.register(board_info.MIC_CLK, fm.fpioa.I2S0_SCLK, force=True)

mic_dev = I2S(I2S.DEVICE_0)
mic_dev.channel_config(mic_dev.CHANNEL_0, mic_dev.RECEIVER, align_mode=I2S.STANDARD_MODE)
mic_dev.set_sample_rate(sample_rate)
print(mic_dev)

#Speaker I2s Initialize
fm.register(board_info.SPK_SD, fm.fpioa.GPIO0)
spk_sd=GPIO(GPIO.GPIO0, GPIO.OUT)
spk_sd.value(1)
fm.register(board_info.SPK_DIN,fm.fpioa.I2S1_OUT_D1)
fm.register(board_info.SPK_BCLK,fm.fpioa.I2S1_SCLK)
fm.register(board_info.SPK_LRCLK,fm.fpioa.I2S1_WS)
wav_dev = I2S(I2S.DEVICE_1)
print(wav_dev)

#Record Wav File
def record_wav(fname):
    lcd.draw_string(20,50,"record_wav")
    print("Record Wav File Start")
    player = audio.Audio(path=fname, is_create=True, samplerate=sample_rate)
    queue = []
    for i in range(200):
        tmp = mic_dev.record(sample_points)
        if len(queue) > 0:
            ret = player.record(queue[0])
            queue.pop(0)
        #lcd.draw_string(20,50,"REC",i)
        mic_dev.wait_record()
        queue.append(tmp)
    player.finish()
    lcd.clear()
    print("Record Wav File finish")

#Play Wav File
def play_wav(fname):
    lcd.draw_string(20,50,"play_wav")
    print("Play Wav File Start")
    player = audio.Audio(path = fname)
    player.volume(100)
    wav_info = player.play_process(wav_dev)
    wav_dev.channel_config(wav_dev.CHANNEL_1,
        I2S.TRANSMITTER,resolution = I2S.RESOLUTION_16_BIT,
        align_mode = I2S.STANDARD_MODE)
    wav_dev.set_sample_rate(sample_rate)
    while True:
        ret = player.play()
        if ret == None:
            break
        elif ret==0:
            break
    player.finish()
    lcd.clear()
    print("Play Wav File finish")

lcd.init()
lcd.clear()
lcd.rotation(2)

but_stu_a = 1
but_stu_b = 1

while(True):
    if but_a.value() == 0 and but_stu_a == 1:
        lcd.clear(236, 36, 36)
        play_wav("record_1.wav")
        but_stu_a = 0
    if but_a.value() == 1 and but_stu_a == 0:
        but_stu_a = 1


    if but_b.value() == 0 and but_stu_b == 1:
        lcd.clear(255,255,0)
        record_wav("record_1.wav")
        but_stu_b = 0
    if but_b.value() == 1 and but_stu_b == 0:
        but_stu_b = 1




