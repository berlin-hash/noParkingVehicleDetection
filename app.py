from flask import Flask, render_template, request
app = Flask(__name__)
import cv2 
import Main
import json
from twilio.rest import Client

with open('./userData/data.json', 'r') as f:
    dataJson = json.load(f)

def findPhoneNumber(plateNumber):
    dict_list = [item for item in dataJson]

    for item in dict_list:
        if(item.get(plateNumber)):
            return item.get(plateNumber)
    
    return None

@app.route('/sms', methods=['POST'])
def send_sms():
    
    plateNumber = request.form['plateNumber']
    phoneNumber = request.form['phoneNumber']
    print(plateNumber, phoneNumber)
    # return None

    account_sid = 'ACda5c7627a70ac945296601c6f0170a9f'
    auth_token = '30207ab77b1761128a6a98ffb6af31b4'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+14754053072',
        body='Your vehicle ' + plateNumber + ' has been prosecuted for NO PARKING at RNSIT Gate. You have been fined Rs.500. Please pay your fine within 7 days.', 
        to='+91'+phoneNumber
    )

    print(message.sid)
    return message.sid

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        image = request.files['image']
        image.save('uploaded_image.jpg')
        print(image.filename)
        # Call the function for image processing
        number_plate = Main.main(image.filename)
        if(number_plate == None):
            return ('No number plate found')
        print(number_plate)
        phoneNumber = findPhoneNumber(number_plate)
        print(phoneNumber)
        # send_sms(number_plate, phoneNumber)
        return render_template('userDisplay.html',plateNumber=number_plate,phoneNumber=phoneNumber )


if __name__ == '__main__':
    app.run(debug=True)
