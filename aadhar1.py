from flask import Flask, render_template, request, jsonify
import os
import cv2
from pyzbar.pyzbar import decode
from pyaadhaar.utils import isSecureQr
from pyaadhaar.decode import AadhaarSecureQr
from datetime import date
import xmltodict



app = Flask(__name__, template_folder='templates')

# Specify the folder where uploaded files will be stored
app.config['/home/aashutosh9178/aadhar/uploads'] = 'uploads'

# Function to process the uploaded image
def process_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    code = decode(gray)
    
    if len(code):
        qrData = code[0].data
    else:
        return None

    isSecureQR = isSecureQr(qrData)
    
    if isSecureQR:
        secure_qr = AadhaarSecureQr(int(qrData))
        QRDATA = secure_qr.decodeddata()
    else:
        QRDATA = xmltodict.parse(qrData.decode())['PrintLetterBarcodeData']

    ret = {}
    year = date.today().year

    for k in QRDATA.keys():
        if 'name' in k:
            ret['name'] = QRDATA[k]
        elif 'dob' in k:
            ret['age'] = year - int(QRDATA[k].split('-')[2])
        elif 'yob' in k:
            ret['age'] = year - int(QRDATA[k])
        elif 'gender' in k:
            ret['gender'] = QRDATA[k]
        elif 'pc' in k or 'pincode' in k:
            ret['pincode'] = QRDATA[k]
        elif 'state' in k:
            ret['state'] = QRDATA[k].lower()
        elif 'mobile' in k:
            ret['mobile'] = QRDATA[k]
        elif 'email' in k:
            ret['email'] = QRDATA[k]
        elif 'vtc' in k:
            ret['vtc'] = QRDATA[k].lower()
        elif 'street' in k:
            ret['street'] = QRDATA[k].lower()
        elif 'adhar_last_digit' in k:
            ret['adhar_last_digit'] = QRDATA[k]

    return ret

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        filename = os.path.join(app.config['/home/aashutosh9178/aadhar/uploads'], file.filename)
        file.save(filename)
        
        result = process_image(filename)
        
        if result:
            return jsonify(result)
        else:
            return jsonify({'error': 'Error processing the image'})
        
        

if __name__ == '__main__':
    app.run(debug=True)
