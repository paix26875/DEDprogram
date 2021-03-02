import numpy as np
from PIL import Image
from icecream import ic
import twocolor_convert as tc

if __name__ == '__main__':
    img_uint = np.array(Image.open("/Users/paix/Desktop/Python_lab/calibration/time_average/colorimg/CMOS_uint8_1600_B.bmp"))
    img_int = np.array(Image.open("/Users/paix/Desktop/Python_lab/calibration/time_average/colorimg/CMOS_int8_1600_B.bmp"))
    img_pyrometer = np.array(Image.open("/Users/paix/Desktop/Python_lab/calibration/time_average/colorimg/1600_11.bmp"))
    
    print(np.all(img_int == img_uint))
    img_error = img_int - img_pyrometer
    ic(img_error.size)
    ic(np.count_nonzero(img_error))
    error_rate = np.count_nonzero(img_error) / img_error.size * 100
    ic(error_rate)

    temp_CMOS = tc.totemperature(img_int)
    temp_CMOS = np.where(temp_CMOS > 2200, 0, temp_CMOS)
    temp_CMOS = np.where(temp_CMOS < 1800, 0, temp_CMOS)
    temp_pyrometer = tc.totemperature(img_pyrometer)
    temp_pyrometer = np.where(temp_pyrometer > 2200, 0, temp_pyrometer)
    temp_pyrometer = np.where(temp_pyrometer < 1800, 0, temp_pyrometer)

    temp_error = temp_pyrometer - temp_CMOS
    ic(np.sum(temp_error))# これ絶対値とる必要あるかも
    ic(np.count_nonzero(temp_CMOS))
    ic(np.sum(temp_error)/np.count_nonzero(temp_CMOS))
    ic(np.max(temp_error))
    ic(np.min(temp_error))

    # print(np.isclose(img_int, img_pyrometer))