import csv
import math
import logging
import requests
import os
import sys
from typing import Optional
from fastapi import FastAPI, Response, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status
import uvicorn
from pydantic import BaseModel
import json
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import datetime
import pandas as pd

app = FastAPI()

#logging.basicConfig(level=logging.INFO, filename='api.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_rmse(url1, url2):
    try:    
        #response1 = requests.get(url1)
        #response2 = requests.get(url2)

        #data1 = response1.text.splitlines()
        #data2 = response2.text.splitlines()

        #reader1 = csv.reader(data1)
        #reader2 = csv.reader(data2)

        #print(reader1)
        #print(reader2)

        #values1 =[]
        #for row in reader1:
        #     values1.append(row[1])

        #values1=values1[1:]

        #values1 = [float(i) for i in values1]

        #print(values1)

        #values2 =[]
        #for row in reader2:
        #     values2.append(row[1])

        #values2=values2[1:]

        #values2 = [float(i) for i in values2]

        #print(values2)

        data1 = pd.read_csv(url1)
        data2 = pd.read_csv(url2)

        values1 = list(data1[data1.columns[1]])
        values2 = list(data2[data2.columns[1]])

        if len(values1) != len(values2):
            raise ValueError("CSV files should have the same number of rows.")

        mse = sum((x - y) ** 2 for x, y in zip(values1, values2)) / len(values1)
        rmse = math.sqrt(mse)

        return rmse
    
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise

@app.get('/')
def entry_point():
    return "Hey"

class CommitPayload(BaseModel):
    url1: Optional[str] = None
    url2: Optional[str] = None

@app.post('/calculate_rmse')
async def api_calculate_rmse(log: CommitPayload):
    log_dict={
        'url1':log.url1,
        'url2': log.url2
    }
    try:
        url1 = log_dict.get('url1')
        url2 = log_dict.get('url2')

        if not url1 or not url2:
            raise ValueError("Missing CSV URLs.")

        rmse = calculate_rmse(url1, url2)
        logging.info(f"RMSE calculated successfully: {rmse}")
        return json.dumps({'rmse': rmse})

    except ValueError as ve:
        logging.error(f"Value Error: {str(ve)}")
        return json.dumps({'error': str(ve)}), 400

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return json.dumps({'error': 'An error occurred.'}), 500

if __name__ == '__main__':
    uvicorn.run(app, port=8080)
