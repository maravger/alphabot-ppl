#!flask/bin/python
from flask import Flask
from flask import request, url_for
from flask import jsonify, abort
from dna import Dna
from werkzeug.utils import secure_filename
from alphabot_exceptions import *
import os 

d = Dna()
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def post_image():
    if request.method == 'GET':
        return "GET \n"
    if request.method == 'POST':
        
        
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(filename)
        dirr = os.getcwd()
        osname = os.path.join(dirr, '')
        dest_img = osname + filename
        try: 
            results = d.find_distance_and_angle(dest_img)  ### pairnei path
            os.remove(dest_img)
            return jsonify(results)
        except BeaconNotFoundError:
            os.remove(dest_img)
            return abort (404)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.114', port=8000)
