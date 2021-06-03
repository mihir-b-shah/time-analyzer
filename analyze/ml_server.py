
from flask import Flask, request, render_template
import logging
import model
import atexit

app = Flask(__name__)
models = {}
logging.basicConfig(level=logging.DEBUG)
curr_id = None
  
def init_if_needed():
  if(curr_id == None):
    raise RuntimeError('no current email found.')
  elif(not(curr_id in models)):
    models[curr_id] = models.UselessModel()
  return models[curr_id]

@app.route('/labeling', methods = ['GET', 'POST'])
def labeling_page():
  website_list = data_model.list_to_label()
  if(request.method == 'GET'):
    return render_template('label.html', websites = website_list)
  elif(request.method == 'POST'):
    data_model = init_if_needed()
    lbls = ['lbl%d'%(i) for i in range(1, 1+len(website_list))]
    res = list(zip(website_list, map(request.form.get, lbls)))
    data_model.process_labels(res);
    app.logger.info(res);
    return 'Thank you for submitting these labels.'
  else:
    pass

@app.route('/decide', methods = ['POST'])
def decide_block():
  jsn = request.get_json()
  curr_id = jsn['id']

  data_model = init_if_needed()
  ret = 'BLOCK' if data_model.insert_and_decide(jsn['id'], jsn['data']) else 'STAY'
  app.logger.info(ret)
  return ret

# exit strategy-handles Ctrl-C signal too
@atexit.register
def interrupt_handler():
  f = open('c:/users/mihir/hello.txt','w')
  f.write('wowwy cowy!')
  f.close()

# run
LocalHostIP = '127.0.0.1'
app.run(host=LocalHostIP, port=5050)
