from flask import Flask, render_template

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return render_template("index.html")

#Auth 
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

@app.route("/government_login")
def government_login():
    return render_template("government_login.html")    

@app.route("/doctor_verification")
def doctor_verification():
    return render_template("doctor_verification.html")

#Patient left panel 
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/appointments')
def appointments():
    return render_template('appointments.html')  

@app.route('/medical-records')
def records():
    return render_template('records.html') 

# @app.route('/communication')
# def communication():
#     return render_template('dashboard.html') 

@app.route('/health-tracking')
def health_tracking():
    return render_template('health.html')  

@app.route('/profile-settings')
def profile_settings():
    return render_template('profile_setting.html')  

@app.route('/support-help')
def support_help():
    return render_template('support_help.html')  

    
if __name__ == "__main__":
    app.run(debug=True)