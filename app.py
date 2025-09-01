from flask import Flask, render_template

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return render_template("index.html")

#Auth 
@app.route("/patient_signup")
def patient_signup():
    return render_template("auth/patient_signup.html")

@app.route("/patient_login")
def patient_login():
    return render_template("auth/patient_login.html")

@app.route("/doctor_signup")
def doctor_signup():
    return render_template("auth/doctor_signup.html")

@app.route("/doctor_login")
def doctor_login():
    return render_template("auth/doctor_login.html")    

@app.route("/government_signup")
def government_signup():
    return render_template("auth/government_signup.html")   

@app.route("/government_login")
def government_login():
    return render_template("auth/government_login.html")    

@app.route("/doctor_verification")
def doctor_verification():
    return render_template("auth/doctor_verification.html")

# Patient left panel 
@app.route('/dashboard')
def dashboard():
    return render_template('patient/dashboard.html')

@app.route('/appointments')
def appointments():
    return render_template('patient/appointments.html')  

@app.route('/medical-records')
def records():
    return render_template('patient/records.html') 

# @app.route('/communication')
# def communication():
#     return render_template('patient/comunication.html') 

@app.route('/health-tracking')
def health_tracking():
    return render_template('patient/health.html')  

@app.route('/profile-settings')
def profile_settings():
    return render_template('patient/profile_setting.html')  

@app.route('/support-help')
def support_help():
    return render_template('patient/support_help.html')  

# Doctor Portal Routes (matching your sidebar files)
@app.route('/doctor_dashboard.html')
def doctor_dashboard():
    return render_template('doctor/doctor_dashboard.html')

@app.route('/doctor_appointments.html')
def doctor_appointments():
    return render_template('doctor/doctor_appointments.html')

@app.route('/doc_patient_records.html')
def doctor_patient_records():
    return render_template('doctor/doc_patient_records.html')

@app.route('/doc_communication.html')
def doctor_communication():
    return render_template('doctor/doc_communication.html')

@app.route('/doctor_prescription.html')
def doctor_prescription():
    return render_template('doctor/doctor_prescription.html')

@app.route('/analytics.html')
def doctor_analytics():
    return render_template('doctor/analytics.html')

@app.route('/profile_setting_doc.html')
def doctor_profile_settings():
    return render_template('doctor/profile_setting_doc.html')

# Government Portal Routes (if needed)
@app.route('/government/dashboard')
def government_dashboard():
    return render_template('government/government_dashboard.html')


if __name__ == "__main__":
    app.run(debug=True)