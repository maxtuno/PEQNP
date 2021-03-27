import sys
import time
import os
import requests
import zipfile

if __name__ == '__main__':

    key = sys.argv[1].replace('.cnf', '')

    zf = zipfile.ZipFile('{}.zip'.format(key), mode='w')
    zf.write('{}.cnf'.format(key))
    zf.close()

    with open('{}.zip'.format(key), 'rb') as file:
        r = requests.post('http://0.0.0.0:5000/satisfy', files={'cnf': file})
        print(r.text)
