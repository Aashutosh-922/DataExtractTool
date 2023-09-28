import cv2
from pyzbar.pyzbar import decode

# Read the QR code image
image = cv2.imread('/home/aashutosh9178/Downloads/WhatsApp Image 2023-09-24 at 7.36.43 PM.jpeg')

# Decode the QR code
decoded_objects = decode(image)

# Loop through the decoded objects (there may be multiple QR codes in an image)
for obj in decoded_objects:
    data = obj.data.decode("utf-8")
    print("Data:", data)
