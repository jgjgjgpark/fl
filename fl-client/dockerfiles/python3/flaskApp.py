from flask import Flask
import requests
app = Flask(__name__)
@app.route("/")
def main():
  r = requests.get('http://169.254.169.254/latest/dynamic/instance-identity/document')
  text = "Welcome! Here is some info about me!\n\n" + r.text
  return text

def test():
  requests.post('', '')


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)
