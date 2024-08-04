from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline
import logging
from logging.handlers import RotatingFileHandler
import traceback

# Set up application and logging
application = Flask(__name__)
app = application

# Configure logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

# Route for homepage
@app.route('/')
def index():
    app.logger.info("Homepage accessed")
    return render_template('home.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        app.logger.info("GET request to /predictdata")
        return render_template('home.html')
    else:
        app.logger.info("POST request to /predictdata")
        try:
            # Log form data (be careful not to log sensitive information in production)
            app.logger.debug(f"Form data: {request.form}")
            
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=float(request.form.get('reading_score')),
                writing_score=float(request.form.get('writing_score'))
            )
            app.logger.debug(f"CustomData object created: {data.__dict__}")
            
            pred_df = data.get_data_as_data_frame()
            app.logger.debug(f"Prediction dataframe: {pred_df.to_dict()}")
            
            predict_pipeline = PredictPipeline()
            app.logger.debug("PredictPipeline object created")
            
            results = predict_pipeline.predict(pred_df)
            app.logger.info(f"Prediction results: {results}")
            
            app.logger.debug(f"Rendering template with results: {results[0]}")
            return render_template('home.html', results=results[0])
        except Exception as e:
            app.logger.error(f"An error occurred: {str(e)}")
            app.logger.error(traceback.format_exc())
            return render_template('home.html', error="An error occurred during prediction. Please try again."), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
