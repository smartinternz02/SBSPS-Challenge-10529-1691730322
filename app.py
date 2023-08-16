import numpy as np
from flask import Flask, request, render_template
import pickle
import io
import base64
import matplotlib.pyplot as plt

flask_app = Flask(__name__)

model = pickle.load(open("Placement.pkl","rb"))

@flask_app.route("/")
def Home():
    return render_template("home.html")


@flask_app.route("/predict", methods = ["GET","POST"])  
def predict():
    b = request.form.get('gender')
    c = request.form.get('ssc_p')
    d = request.form.get('ssc_b')
    e = request.form.get('hsc_p')
    f = request.form.get('hsc_b')
    g = request.form.get('hsc_s')
    h = request.form.get('degree_p')
    i = request.form.get('degree_t')
    j = request.form.get('workex')
    k = request.form.get('etest_p')
    l = request.form.get('specialisation')
    m = request.form.get('mba_p')
  
    if b=='' or c=='' or d=='' or e=='' or f=='' or g=='' or h=='' or i=='' or j=='' or k=='' or l=='' or m=='':
        return "You can't leave any field empty!!!"

    b = int(b)
    c = float(c)
    d = int(d)
    e = float(e)
    f = int(f)
    g = int(g)
    h = float(h)
    i = int(i)
    j = int(j)
    k = float(k)
    l = int(l)
    m = float(m)

    import requests

    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "6GqMSDvRbT0n8jy2Gl7cuCE3d7D3BDgiUTL-X-0suZkP"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
    API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": ["gender","ssc_p","ssc_b","hsc_p","hsc_b","hsc_s","degree_p","degree_t","workex","etest_p","specialisation","mba_p"], "values": [[b,c,d,e,f,g,h,i,j,k,l,m]]}]}

    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/810c2eba-abae-4a6b-a505-e294f30a7a5f/predictions?version=2021-05-01', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    pred=response_scoring.json()
    prediction=pred['predictions'][0]['values'][0][0]

    categories = ['ssc_p', 'hsc_p', 'degree_p', 'etest_p', 'mba_p']
    values1 = [c, e, h, k, m]

    fig, ax = plt.subplots()
    bar_width = 0.40
    x = np.arange(len(categories))
    ax.bar(x - bar_width/2, values1, bar_width, label='percentage you got in each exams')
    ax.set_title('Bar Plot')
    ax.set_xlabel('Exams')
    ax.set_ylabel('Percentage')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()

    # Encode the plot image as base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template("after.html", data=prediction,plot_url=plot_url)

if __name__ == "__main__":
    flask_app.run(debug=True)