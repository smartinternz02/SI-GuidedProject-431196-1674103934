import pickle 
from flask import Flask,render_template,request
import requests
import json
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "tO3Odab6caxUAezVXS6CZ1_KELSygxz47Ea-2TyCcnPD"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

model=pickle.load(open("model.pkl","rb"))
app = Flask(__name__)

@app.route('/')
def predict(): 
    return render_template("predict.html")
@app.route('/predict',methods=['POST'])
def pred():
    d=request.form['department']
    if d=="Sales & Marketing":
       d=7
    elif d=="Operations":
       d=4
    elif d=="Technology":
       d=8
    elif d=="Analytics":
       d=0
    elif d=="R&D":
       d=6    
    elif d=="Procurement":
       d=5
    elif d=="Finance":
       d=1
    elif d=="HR":
       d=2
    elif d=="Legal":
       d=3
    education=request.form['education']

    if education == '1': 
        education = 1

    elif education == '2':

        education = 2

    else:

        education = 3


    no_of_trainings = request.form['no_of_trainings']

    age= request.form['age']

    previous_year_rating = request.form["previous_year_rating"]
    length_of_service = request.form["length_of_service"]

    KPIS= request.form['KPIs']

    if KPIS == '0':

        KPIS = 8

    else:

        KPIs = 1

    awards_won=request.form['awards_won']

    if awards_won == '0': awards_won = 0

    else:

        awards_won = 1

    avg_training_score = request.form['avg_training_score']

    total = [[float(d), float(education), float(no_of_trainings), float(age), float(previous_year_rating), float (length_of_service),

              KPIs, awards_won, avg_training_score]]

    payload_scoring = {"input_data": [{"field": [["department","education","no_of_trainings","age","previous_year_rating","length_of_service","KPIs_met >80%","awards_won?","avg_training_score]"]], "values": total}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/6b18c84f-08b1-440c-8f0e-6a574705173e/predictions?version=2023-02-08', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predict=response_scoring.json()
    pred=predict['predictions'][0]['values'][0][0]
    if pred==0:
        text = 'Sorry, you are not eligible for promotion'

    else:
        text = 'Great, you are eligible for promotion'
    return render_template("submit.html",data=text)
if __name__== '__main__' :
    app.run(debug=True)

