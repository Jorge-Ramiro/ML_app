from flask import Flask, request, render_template
import json
from model import Model

app = Flask(__name__)

model = Model()

@app.route("/")
def home():
    return render_template("main.html")


@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    result = json.loads(output)
    result = model.predict(result['arr'])
    return result



if __name__ == '__main__':
    app.run(debug=True)