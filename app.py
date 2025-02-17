import os
import shutil
import random
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024
app.secret_key = 'supersecretkey'

if(not os.path.exists(app.config['UPLOAD_FOLDER'])):
  os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def upload_file():
  success = None
  if(request.method == 'POST'):
    if('file' not in request.files):
      flash('No file part')
      return redirect(request.url)
    
    file = request.files['file']

    if(file.name == ''):
      flash('No selected file')
      return redirect(request.url)
    
    if(file):
      for item in os.listdir("uploads"):
        item_path = os.path.join('uploads', item)

        # Remove Directories and their contents
        if(os.path.isdir(item_path)):
          shutil.rmtree(item_path)
        else:
          os.remove(item_path)
          
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
      messages = ["Yes", "Done", "successful", "Good", "Well Done"]
      random.shuffle(messages)
      success = random.choice(messages)
      flash(f"File {file.filename} uploaded successfully!")
      # return redirect(url_for('upload_file'))
  
  return render_template('index.html', msg = success)

if(__name__ == "__main__"):
  app.run(debug=True)

