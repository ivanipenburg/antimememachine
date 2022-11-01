'''
How to run Flask server:
1. Stay in main '/antimememachine/' folder
2. >> $env:FLASK_APP = "main.py"
3. >> $env:FLASK_ENV = "development"
4. >> venv/Scripts/activate
5. >> cd backend
6. >> flask run
'''

from webbrowser import get

from flask import Flask, jsonify, request
from flask_cors import CORS

from torch_utils import get_prediction, transform_image

app = Flask(__name__)
CORS(app)

def allowed_filename(filename):
    '''Check if file is allowed'''
    allowed_extensions = ['png', 'jpg', 'jpeg']
    for ext in allowed_extensions:
        if ext in filename:
            return True
    return False


def get_class_name(index):
    '''Get class name from index'''
    class_names = {0: 'AlwaysHasBeen', 1: 'AnakinPadme4Panel', 2: 'BatmanSlappingRobin', 3: 'BernieIAmOnceAgainAskingForYourSupport', 4: 'BikeFall', 5: 'BlankNutButton', 6: 'BoardroomMeetingSuggestion', 7: 'BuffDogevs.Cheems', 8: 'ChangeMyMind', 9: 'ClownApplyingMakeup', 10: 
'DisasterGirl', 11: 'DistractedBoyfriend', 12: 'DrakeHotlineBling', 13: 'EpicHandshake', 14: 'ExpandingBrain', 15: "Gru'sPlan", 16: 'GuyHoldingCardboardSign', 17: 'HidethePainHarold', 18: "IBetHe'sThinkingAboutOtherWomen", 19: 'InhalingSeagull', 20: 'IsThisAPigeon', 21: 'LeftExit12OffRamp', 22: 'Megamindpeeking', 23: 'MockingSpongebob', 24: 'MonkeyPuppet', 25: 'OneDoesNotSimply', 26: 'Other', 27: 'PanikKalmPanik', 28: 'RunningAwayBalloon', 29: 'SadPabloEscobar', 30: 'TheScrollOfTruth', 31: "They'reTheSamePicture", 32: 'ThisIsFine', 33: 'TradeOffer', 34: 'TuxedoWinnieThePooh', 35: 'TwoButtons', 36: 'UNODraw25Cards', 37: 'WaitingSkeleton', 38: 'WillSmithpunchingChrisRock', 39: 'WomanYellingAtCat', 40: 'X,XEverywhere'}
    return class_names[index]


@app.route('/predict', methods=['POST'])
def predict():
    '''Predict meme class'''
    if request.method == 'POST':
        file = request.files.get('file')

        if file is None or file.filename == '':
            response = jsonify({'error': 'no file'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        if not allowed_filename(file.filename):
            response = jsonify({'error': 'format not supported'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
    
        try:
            img_bytes = file.read()
            tensor = transform_image(img_bytes)
            prediction = get_prediction(tensor)
            predicted_class = prediction.item()
            data = {'prediction': predicted_class, 'class_name': get_class_name(predicted_class)}
            response = jsonify(data)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            response = jsonify({'error': message})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
