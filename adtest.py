import cv2
from pyzbar.pyzbar import decode
from pyaadhaar.utils import isSecureQr
from pyaadhaar.decode import AadhaarSecureQr

img = cv2.imread('/home/aashutosh9178/Downloads/Screenshot_2023-09-24-18-41-42-172_com.google.android.apps.docs.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

code = decode(gray)
qrData = code[0].data

isSecureQR = (isSecureQr(qrData))

if isSecureQR:
    secure_qr = AadhaarSecureQr(int(qrData))
    decoded_secure_qr_data = secure_qr.decodeddata()
    print(decoded_secure_qr_data)
