from flask import Flask,render_template,request

app=Flask(__name__)

import pickle

model=pickle.load(open("promotion.pkl","rb"))


@app.route('/')
def index():
    return render_template("main_index.html")

@app.route('/datas',methods=["POST"])
def do():
    d=request.form["dept"]
    
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
        
        
    num_of_training=request.form["not"]
    pre_yr_rating=request.form["pyr"]
    len_of_service=request.form["los"]
    kpi=request.form["kpi"]
    award=request.form["aw"]
    avg_training_score=request.form["ats"]
    
    data=[[d,num_of_training,pre_yr_rating,len_of_service,kpi,award,avg_training_score]]
    
    p=model.predict(data)
    
    if p == 0:
        text = 'Sorry, you are not eligible for promotion'
    else:
        text = 'Great, you are eligible for promotion'

    
    return render_template("main_index.html",data=text)

app.run(debug=True)