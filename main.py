from flask import Flask, json, request

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

filename = "hello.json"

app = Flask(__name__)

@app.route('/health/')
def healthCheck():
    return "Alive", 200

@app.route('/companies')
def home():
    return json.dumps(companies)

@app.route('/companies', methods=['POST'])
def add_income():
    companies.append(request.get_json())
    return '', 200

@app.route("/file", methods=['GET', 'POST'])
def file():
    if request.is_json:
        rqst = request.get_json()
        with open(filename, "a") as myfile:
            json.dump(rqst, myfile)
        return "OK", 200
    return {"error": "Request must be JSON"}, 415

if __name__ == "__main__":
    app.run(debug=True)