import numpy as np
from KW import KW

def log(label, val):
    print(f"[{label}]: {val}")

ip = "192.168.15.49"

camera = KW.Camera()
ret = camera.connect(ip)
log("connect", ret)

if ret != 0:
    print("Connection failed, exiting.")
    exit(1)

# Read config and get capture num
config_read = []
status_read = []
capture_num = []
ret = camera.readJson(config_read, "./config.json")
log("readJson", ret)
ret = camera.setParamJson(config_read[0], status_read, capture_num)
log("setParamJson", ret)

# Get calibration
calib_param = KW.CalibrationParam()
ret = camera.getCalibrationParam(calib_param)
log("getCalibrationParam", ret)

if ret == 0:
    intrinsic_flat = KW.get_intrinsic(calib_param)
    extrinsic_flat = KW.get_extrinsic(calib_param)
    distortion     = KW.get_distortion(calib_param)

    log("intrinsic (flat)", intrinsic_flat)
    log("extrinsic (flat)", extrinsic_flat)
    log("distortion (flat)", distortion)

    K  = np.array(intrinsic_flat, dtype=np.float32).reshape(3, 3)
    RT = np.array(extrinsic_flat, dtype=np.float32).reshape(4, 4)
    D  = np.array(distortion, dtype=np.float32)[:5]

    print("\nK (3x3 intrinsic matrix):\n", K)
    print("\nRT (4x4 extrinsic matrix):\n", RT)
    print("\nD (5 distortion coeffs):", D)
else:
    print("getCalibrationParam failed.")

camera.disconnect(ip)