import os
import time
import zipfile
import subprocess

from flask import Flask, request

app = Flask(__name__)

app.config['ALLOWED_EXTENSIONS'] = {'zip', 'cnf', 'mod'}
app.config['UPLOAD_FOLDER'] = 'uploads/'


@app.route('/satisfy', methods=['POST'])
def satisfy():
    cnf = request.files['cnf']
    filename = '{}.zip'.format(time.time())
    cnf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    try:
        with zipfile.ZipFile(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as zf:
            zf.extractall(os.path.join(app.config['UPLOAD_FOLDER']))
    except zipfile.BadZipfile as e:
        print(e)
        return "", 406
    subprocess.call('java -jar -Xmx4g {0}/blue.jar {0}/{1}.cnf > {0}/{1}.mod'.format(os.path.join(app.config['UPLOAD_FOLDER'], ''), 'remote'), shell=True)
    with open(os.path.join(app.config['UPLOAD_FOLDER'], 'remote.mod'), 'r') as file:
        return file.read()


if __name__ == '__main__':
    app.run()
