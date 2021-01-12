
from flask import Flask, request, render_template
import model

app = Flask(__name__)
data_model = model.Model('useless')
    
@app.route('/labeling', methods = ['GET', 'POST'])
def labeling_page():
    website_list = data_model.list_to_label()
    if(request.method == 'GET'):
        return render_template('label.html', websites = website_list)
    elif(request.method == 'POST'):
        lbls = ['lbl%d'%(i) for i in range(1, 1+len(website_list))]
        data_model.process_labels(list(zip(website_list, map(request.form.get, lbls))))
        return 'Thank you for submitting these labels.'
    else:
        pass

@app.route('/decide', methods = ['POST'])
def decide_block():
    jsn = request.get_json()
    return 'BLOCK' if data_model.insert_and_decide(jsn['id'], jsn['data']) else 'STAY'

LocalHostIP = '127.0.0.1'
app.run(host=LocalHostIP, port=5050)