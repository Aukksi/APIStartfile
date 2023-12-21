import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/')
def index():
   #print('Moro')
  try:
    os.system(f'python {/paivansoppa.py}')
    return 'Joo'
  except FileNotFoundError:
    
    return 'Ei'


#@app.route('/hello', methods=['GET'])
#def hello():
#  os.system(f'python {/paivansoppa.py}')

if __name__ == '__main__':
   app.run()
