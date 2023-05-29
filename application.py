import csv
import math
import logging
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

#logging.basicConfig(level=logging.INFO, filename='api.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_rmse(url1, url2):
    try:    
        response1 = requests.get(url1)
        response2 = requests.get(url2)

        data1 = response1.text.splitlines()
        data2 = response2.text.splitlines()

        reader1 = csv.reader(data1)
        reader2 = csv.reader(data2)

        print(reader1)
        print(reader2)

        values1 =[]
        for row in reader1:
             values1.append(row[1])

        values1=values1[1:]

        values1 = [float(i) for i in values1]

        print(values1)

        values2 =[]
        for row in reader2:
             values2.append(row[1])

        values2=values2[1:]

        values2 = [float(i) for i in values2]

        print(values2)

        if len(values1) != len(values2):
            raise ValueError("CSV files should have the same number of rows.")

        mse = sum((x - y) ** 2 for x, y in zip(values1, values2)) / len(values1)
        rmse = math.sqrt(mse)

        return rmse
    
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise

@app.route('/', methods=['GET'])
def entry_point():
    return "Hey"

@app.route('/calculate_rmse', methods=['POST'])
def api_calculate_rmse():
    try:
        data = request.get_json()
        url1 = data.get('url1')
        url2 = data.get('url2')

        if not url1 or not url2:
            raise ValueError("Missing CSV URLs.")

        rmse = calculate_rmse(url1, url2)
        logging.info(f"RMSE calculated successfully: {rmse}")
        return jsonify({'rmse': rmse})

    except ValueError as ve:
        logging.error(f"Value Error: {str(ve)}")
        return jsonify({'error': str(ve)}), 400

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred.'}), 500

if __name__ == '__main__':
    app.run(port=8080)
