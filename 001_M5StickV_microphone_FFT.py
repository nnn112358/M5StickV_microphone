##fork <https://gist.github.com/ksasao/3dbb900ea10baa05930e12291da2db0a>

import audio
import sys
import lcd
from fpioa_manager import *
from Maix import I2S, GPIO, FFT

lcd.init()
lcd.rotation(2)

# mic setup
sample_points = 1024
sample_rate = 38640
FFT_points = 512

# I2S MIC GPIO
fm.register(board_info.MIC_LRCLK, fm.fpioa.I2S0_WS, force=True)
fm.register(board_info.MIC_DAT, fm.fpioa.I2S0_IN_D0, force=True)
fm.register(board_info.MIC_CLK, fm.fpioa.I2S0_SCLK, force=True)

rx = I2S(I2S.DEVICE_0)
rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode = I2S.STANDARD_MODE)
rx.set_sample_rate(sample_rate)

img = image.Image()
lcd_width = 240
lcd_height = 135
hist_num = FFT_points #changeable
if hist_num > 240:
    hist_num = 240
hist_width = int(480 / hist_num)#changeable
x_shift = 0
while True:
    audio = rx.record(sample_points)
    FFT_res = FFT.run(audio.to_bytes(),FFT_points)
    FFT_amp = FFT.amplitude(FFT_res)
    img = img.clear()
    x_shift = 0
    for i in range(hist_num):
        if FFT_amp[i] > 135:
            hist_height = 135
        else:
            hist_height = FFT_amp[i]
        img = img.draw_rectangle((x_shift,135-hist_height,hist_width,hist_height),[255,255,255],2,True)
        x_shift = x_shift + hist_width
    lcd.display(img)
    FFT_amp.clear()
