
from flask import Flask, request, render_template
import logging
import model
import atexit
import re
import os
import utils

app = Flask(__name__)
models = {}
logging.basicConfig(level=logging.DEBUG)
curr_id = None
  
def init_if_needed():
  if(curr_id == None):
    raise RuntimeError('email not present.')
  elif(not(curr_id in models)):
    models[curr_id] = model.UselessModel()
  return models[curr_id]

def update_curr_id(cid):
  print(cid)
  end = cid.find('@gmail.com')
  if(end != -1):
    global curr_id
    curr_id = re.sub(r'\W+', '', cid[:end])
  else:
    raise RuntimeError('Non-gmail email address.')

@app.route('/labeling', methods = ['GET', 'POST'])
def labeling_page():
  data_model = init_if_needed()
  website_list = data_model.list_to_label()

  if(request.method == 'GET'):
    return render_template('label.html', websites = website_list)
  elif(request.method == 'POST'):
    lbls = ['lbl%d'%(i) for i in range(1, 1+len(website_list))]
    res = list(zip(website_list, map(request.form.get, lbls)))
    data_model.process_labels(res);
    app.logger.info(res);
    return 'Thank you for submitting these labels.'
  else:
    pass

def log(msg):
  f = open('log.txt', 'a')
  f.write(msg)
  f.write('\n')
  f.close()

@app.route('/decide', methods = ['POST'])
def decide_block():
  jsn = request.get_json()
  update_curr_id(jsn['id'])

  data_model = init_if_needed()
  ret = 'BLOCK' if data_model.insert_and_decide(jsn['id'], jsn['data']) else 'STAY'
  app.logger.info(ret)
  return ret
  
def user_dir_path(email):
  return utils.get_path('models/users/%s'%(email))

# exit strategy-handles Ctrl-C signal too
@atexit.register
def interrupt_handler():
  for (email, model_) in models.items():
    dir_path = user_dir_path(email)
    if(not(os.path.exists(dir_path))):
      os.path.makedirs(dir_path)
    model_.save(dir_path)

# run
LocalHostIP = '127.0.0.1'
app.run(host=LocalHostIP, port=5050)
