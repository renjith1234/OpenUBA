'''
Copyright 2019-Present The OpenUBA Platform Authors
This file is part of the OpenUBA Platform library.
The OpenUBA Platform is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
The OpenUBA Platform is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public License
along with the OpenUBA Platform. If not, see <http://www.gnu.org/licenses/>.
'''


'''
@name process
@description Process engine is the default state of the system, whereby it will ingest
logs into the system

'''
import logging
from dataset import Dataset, DatasetSession, CoreDataFrame
from typing import Dict, Tuple, Sequence, List
from enum import Enum
from entity import GetAllEntities
from user import GetAllUsers

dataset_scheme: dict = {
    "mode": "test",
    "folder": "../test_datasets/toy_1",
    "data":
        [
            {
                "log_name": "proxy",
                "type": "csv",
                "location_type": "disk",
                "folder": "proxy",
                "id_feature": "cs-username"
            }
        ]
}

'''
@name DataSourceFileType
@description eum for data source file type
'''
class DataSourceFileType(Enum):
    CSV = "csv"
    FLAT = "flat"
    PARQUET = "parquet"


'''
@name DataSource
@description class that holds representations for data sources
'''
class DataSource:
    def __init__(self):
        pass


class ProcessEngine():

    def __init__(self):
        logging.info("Process engine is initiated")

    '''
    @name execute
    @description run the process engine, which loads data
    '''
    def execute(self):
        logging.info("executing process engine")
        data_folder = dataset_scheme["folder"]

        # load data from scheme above
        for log_obj in dataset_scheme["data"]:
            log_file_data: CoreDataFrame = self.process_data(data_folder, log_obj)
            logging.warning("dataframe shape: "+str(log_file_data.data.shape))

        # with the CoreDataFrame from process data, perform user/entity analysis/extraction
        # get entities, and users
        all_entities: dict = GetAllEntities().get()
        all_users: dict = GetAllUsers().get()


        # after read the data, perform entity analysis using Entity types

        # adjust risk per entity

    '''
        @name process_data
        @param data_folder: str - the folder holding the files
        @param log_data_obj: dict - log config from the log set
        @description update the current data in the system for each log type.
        This means that we will load a new set of records into the system
    '''
    def process_data(self, data_folder: str, log_data_obj: dict) -> CoreDataFrame:

        logging.warning("Processing Data for : "+str(data_folder))

        log_name = log_data_obj["log_name"]
        log_type = log_data_obj["type"]
        location_type = log_data_obj["location_type"]
        folder = log_data_obj["folder"]
        id_feature = log_data_obj["id_feature"]

        dataset_session = DatasetSession(log_type)

        #read dataset, if any new
        if log_type == DataSourceFileType.CSV.value:
            # invoke datasetsession to read the csv
            dataset_session.read_csv(data_folder, folder, location_type) # load
            print( "isinstance(dataset_session.dataset, Dataset): "+str(isinstance(dataset_session.dataset, Dataset)) )
            dataset_size: Tuple = dataset_session.get_size()
            logging.info( "Dataset Session size: "+str(dataset_size) )


        # fetch actual dataframe
        print("======GET DATAFRAME ======")
        return dataset_session.get_dataset().get_dataframe()
