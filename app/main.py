from fastapi import FastAPI, File, UploadFile
from starlette.responses import RedirectResponse
import pandas as pd
import requests
import json


#from io import StringIO

#from . import crud, models, schemas
#from .database import SessionLocal, engine

app = FastAPI()
url='https://api.postcodes.io/postcodes'

time_exec = pd.to_datetime('today')

# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()





@app.get("/")
def raiz():
    return RedirectResponse(url="/docs/")

@app.get("/validar/{numero}")
def validar_capicua(numero:str):
    respuesta = "No es capicúa"
    if numero==numero[::-1]:
        respuesta = "Es capicúa"
    return {
        "numero":numero,
        "validacion":respuesta
    }

def guardar_archivo_inicial(df):
    df.rename(columns = {'lon':'longitude','lat':'latitude'}, inplace=True)
    df = df.loc[:,('longitude','latitude')]
    df['load_date'] = time_exec
    df.to_sql('geoloaded', con='mysql+mysqlconnector://root:pwd@db:3306/local_db', if_exists='append', index=False)

def guardar_geo_codigopostal(df):
    df['load_date'] = time_exec
    df.to_sql('geoprocessed', con='mysql+mysqlconnector://root:pwd@db:3306/local_db', if_exists='append', index=False)


def consultar_codigopostal(df):
    df.rename(columns = {'lon':'longitude','lat':'latitude'}, inplace=True)
    df['limit'] = 1

    df_l2 = []
    p_json = []
    returned_data = []
    returned_data_tmp = []
    
    
    ctr_carguebd = 10000


    n_rec = 100
    for i in range(0,len(df),n_rec):
        df_l2 = pd.Series([df.iloc[i:i+n_rec].to_dict(orient="records")], index=["geolocations"])
        p_json = json.loads(df_l2.to_json(orient="index"))
        response = requests.post(url, json = p_json)
        response_json = response.json()
        
        
        print(i,i+100)
        
        for j in range(len(response_json['result'])):
            if response_json['result'][j]['result'] is None:
                returned_data_tmp.append([response_json['result'][j]['query']['longitude'],response_json['result'][j]['query']['latitude'],'NOT FOUND'])
            else:
                returned_data_tmp.append([response_json['result'][j]['query']['longitude'],response_json['result'][j]['query']['latitude'],response_json['result'][j]['result'][0]['postcode']])
        
        returned_data = returned_data_tmp

        if len(returned_data_tmp) == ctr_carguebd:
            df_wps_tmp = pd.DataFrame(returned_data_tmp, columns=['longitude','latitude','postalcode'])   
            guardar_geo_codigopostal(df_wps_tmp) 
            returned_data_tmp = []

    if len(returned_data_tmp) > 0 :
        df_wps_tmp = pd.DataFrame(returned_data_tmp, columns=['longitude','latitude','postalcode'])   
        guardar_geo_codigopostal(df_wps_tmp)     
        
        
    df_wps = pd.DataFrame(returned_data, columns=['longitude','latitude','postalcode'])
    df_notf = pd.Series([df_wps.loc[df_wps['postalcode']=='NOT FOUND'].to_dict(orient="records")], index=["result"])
    js_notf = json.loads(df_notf.to_json(orient="index"))
    
    return js_notf

@app.post("/uploadfile/")
async def create_upload_file(u_file: UploadFile):
    #df = pd.read_csv(StringIO(str(file.file.read(), 'utf-16')), encoding='utf-16')
    df = pd.read_csv(u_file.file)
    guardar_archivo_inicial(df)
    js_ret = consultar_codigopostal(df)
    return js_ret

