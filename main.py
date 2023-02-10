from flask import Flask, request, render_template
import json
from model import Model

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("main.html")

model = Model()
predicted = None
@app.route('/prediction', methods=['POST', "GET"])
def prediction():
    global predicted
    if request.method == "POST":
        c_output = request.get_json()
        result = json.loads(c_output)
        predicted = model.predict(result['arr'])
        return predicted
    else:
        return {"breed":predicted}


if __name__ == '__main__':
    app.run(debug=True)