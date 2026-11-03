from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load the trained Random Forest model
with open('heart_failure_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        form_data = {
            'age': request.form['age'],
            'anaemia': request.form['anaemia'],
            'creatinine_phosphokinase': request.form['creatinine_phosphokinase'],
            'diabetes': request.form['diabetes'],
            'ejection_fraction': request.form['ejection_fraction'],
            'high_blood_pressure': request.form['high_blood_pressure'],
            'platelets': request.form['platelets'],
            'serum_creatinine': request.form['serum_creatinine'],
            'serum_sodium': request.form['serum_sodium'],
            'sex': request.form['sex'],
            'smoking': request.form['smoking'],
            'time': request.form['time'],
        }

        # Parse to numbers
        age = float(form_data['age'])
        anaemia = int(form_data['anaemia'])
        creatinine_phosphokinase = float(form_data['creatinine_phosphokinase'])
        diabetes = int(form_data['diabetes'])
        ejection_fraction = float(form_data['ejection_fraction'])
        high_blood_pressure = int(form_data['high_blood_pressure'])
        platelets = float(form_data['platelets'])
        serum_creatinine = float(form_data['serum_creatinine'])
        serum_sodium = float(form_data['serum_sodium'])
        sex = int(form_data['sex'])
        smoking = int(form_data['smoking'])
        time = float(form_data['time'])

        # Create feature array in the correct order (must match training order)
        features = np.array([[
            age, anaemia, creatinine_phosphokinase, diabetes,
            ejection_fraction, high_blood_pressure, platelets,
            serum_creatinine, serum_sodium, sex, smoking, time
        ]])

        # Make prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]

        # Format result
        if prediction == 0:
            result = "Low Risk"
            result_detail = "Patient is likely to survive. Continue regular monitoring."
            confidence = probability[0] * 100
            result_class = "low-risk"
        else:
            result = "High Risk"
            result_detail = "Patient needs immediate medical attention."
            confidence = probability[1] * 100
            result_class = "high-risk"

        return render_template('index.html',
                               prediction_text=result,
                               prediction_detail=result_detail,
                               confidence=round(confidence, 1),
                               result_class=result_class,
                               form_data=form_data)

    except Exception as e:
        return render_template('index.html',
                               prediction_text="Error",
                               prediction_detail="Please check all inputs and try again.",
                               result_class="error",
                               form_data=request.form)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
