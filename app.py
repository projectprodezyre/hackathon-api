import csv
import math
import logging
import requests
import numpy as np

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='api.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_rmse(file1, file2):
    try:
        with open(file1.filename, 'r') as f:
            file_content = f.read()
    
        file1 = file_content.split("\n")
        values1 = file1[0:-1]
        values1 = [float(i) for i in values1]

        with open(file2.filename, 'r') as f:
            file_content = f.read()

        file2 = file_content.split("\n")
        values2 = file2[0:-1]
        values2 = [float(i) for i in values2]

        if len(values1) != len(values2):
            raise ValueError("CSV files should have the same number of rows.")

        MSE = np.square(np.subtract(values1,values2)).mean() 
        rmse = math.sqrt(MSE)

        return rmse

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise


@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    file1 = request.files['file1']
    file2 = request.files['file2']

     # Save the uploaded files
    file1.save(file1.filename)
    file2.save(file2.filename)
    
    rmse = calculate_rmse(file1, file2)
    logging.info(f"RMSE calculated successfully: {rmse}")
    
    # Process the uploaded files (you can perform any desired operations here)
    # For example, you can use libraries like pandas to read and manipulate CSV data
    
    return jsonify({'rmse': rmse})

if __name__ == '__main__':
    app.run(debug=True)
