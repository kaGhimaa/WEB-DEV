from flask import Flask, render_template, request, redirect, jsonify
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['AlgeriaData']
@app.route('/second_page')
def second_page():
    return render_template('second_page.html')

@app.route('/carte_natio')
def carte_natio():
    wilayas = list(db.wilayas.find({}, {'_id': 0, 'Name_Wilaya': 1}))
    return render_template('carte_natio.html', wilayas=wilayas)

@app.route('/get_dairas/<wilaya>', methods=['GET'])
def get_dairas(wilaya):
    wilaya_doc = db.wilayas.find_one({'Name_Wilaya': wilaya})
    dairas = list(db.dairas.find({'ID_Wilaya': wilaya_doc['ID']}, {'_id': 0, 'Name_Daira': 1}))
    return jsonify([daira['Name_Daira'] for daira in dairas])

@app.route('/get_baladias/<daira>', methods=['GET'])
def get_baladias(daira):
    daira_doc = db.dairas.find_one({'Name_Daira': daira})
    baladias = list(db.baladias.find({'ID_Daira': daira_doc['ID']}, {'_id': 0, 'Name_Baladia': 1}))
    return jsonify([baladia['Name_Baladia'] for baladia in baladias])

@app.route('/submit', methods=['POST'])
def submit():
    # Handle form submission
    return 'Form submitted!'



if __name__ == '__main__':
    app.run(debug=True)
