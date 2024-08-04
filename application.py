from flask import Flask, request, render_template
import logging
from logging.handlers import RotatingFileHandler
import traceback

# Initialize the Flask application
app = Flask(__name__)

# Set up logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

# Define routes
@app.route('/')
def index():
    app.logger.info("Homepage accessed")
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        app.logger.info("GET request to /predictdata")
        return render_template('home.html')
    else:
        app.logger.info("POST request to /predictdata")
        try:
            # Log form data
            app.logger.debug(f"Form data: {request.form}")

            # Extract form data
            gender = request.form.get('gender')
            ethnicity = request.form.get('ethnicity')
            parental_level_of_education = request.form.get('parental_level_of_education')
            lunch = request.form.get('lunch')
            test_preparation_course = request.form.get('test_preparation_course')
            writing_score = float(request.form.get('writing_score'))
            reading_score = float(request.form.get('reading_score'))

            # Create data frame or process data for prediction
            # For demonstration purposes, we're just echoing back the input data
            prediction = f"Predicted Maths Score based on inputs: {gender}, {ethnicity}, {parental_level_of_education}, {lunch}, {test_preparation_course}, Writing Score: {writing_score}, Reading Score: {reading_score}"

            app.logger.info(f"Prediction result: {prediction}")

            # Render the result
            return render_template('home.html', results=prediction)
        except Exception as e:
            app.logger.error(f"An error occurred: {str(e)}")
            app.logger.error(traceback.format_exc())
            return render_template('home.html', error="An error occurred during prediction. Please try again."), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
