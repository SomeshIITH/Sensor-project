import os
import sys
import pandas as pd
import numpy as np
from pymongo import MongoClient


from zipfile import Path  #as finally this will return path of csv file

from src.constant import *
from src.utils.main_utils import MainUtils
from src.exception import CustomException
from src.logger import logging

from dataclasses import dataclass 
''' with help of dataclass we can create class without __init__ method  ,just tell parameter datatype and name'''


@dataclass
class DataIngestionConfig:
    artifact_folder :str = os.path.join(artifact_folder)
    

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.utils = MainUtils()
        
    def export_collection_as_dataframe(self,collection_name,db_name):
        
        try:
            mongo_client = MongoClient(url)
            collection = mongo_client[db_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            
            if '_id' in df.columns.to_list():
                df.drop('_id',axis=1,inplace=True)
                
            df.replace("na" ,np.nan,inplace=True)
            
            return df
        
        except Exception as e:
            raise CustomException(e,sys)
    
    
    def export_data_into_feature_store_file_path(self)->pd.DataFrame:
        
        try:
            logging.info(f"Exporting data from Mongo DB") 
            raw_file_path = self.data_ingestion_config.artifact_folder
            os.makedirs(raw_file_path,exist_ok=True)   #if artifact already exist , not give erroe
            
            sensor_data = self.export_collection_as_dataframe(COLLECTION_NAME,DATABASE_NAME)
            
            logging.info(f"saving exported data into feature store file path :{raw_file_path}")
            
            feature_store_file_path = os.path.join(raw_file_path,"wafer_fault.csv")
            
            sensor_data.to_csv(feature_store_file_path,index=False)   #we dont need index
            
            return feature_store_file_path
        
        except Exception as e:
            raise CustomException(e,sys)
        
    
    def initiate_data_ingestion(self)->Path:
        
        logging.info("Entered initiated_data_ingestion method of data_integration class")
        
        try:
            feature_store_file_path = self.export_data_into_feature_store_file_path()
            
            logging.info("got the data from mongodb")
            logging.info("exited initiate_data_ingestion methos of data ingestion class")
            
            return feature_store_file_path
        
        except Exception as e:
            raise CustomException(e,sys)
                      
                    
