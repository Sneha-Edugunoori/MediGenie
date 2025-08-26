from flask import Flask, render_template

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/patient_signup")
def patient_signup():
    return render_template("patient_signup.html")

@app.route("/patient_login")
def patient_login():
    return render_template("patient_login.html")

@app.route("/doctor_signup")
def doctor_signup():
    return render_template("doctor_signup.html")

@app.route("/doctor_login")
def doctor_login():
    return render_template("doctor_login.html")    

@app.route("/government_signup")
def government_signup():
    return render_template("government_signup.html")    
    

if __name__ == "__main__":
    app.run(debug=True)
