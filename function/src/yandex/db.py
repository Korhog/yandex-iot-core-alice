# Yandex DB integration test
from dotenv import load_dotenv
load_dotenv()

import os
import ydb
import ydb.iam
import ast

UPSERT_SQL = """
DECLARE $dev_id AS String;
DECLARE $dev_state AS String;

UPSERT INTO device_capability_states (key, state) VALUES ($dev_id, $dev_state);"""

SELECT_SQL = """
DECLARE $dev_id AS String;

SELECT state FROM device_capability_states WHERE key = $dev_id;
"""

class YDBContext:
    @staticmethod
    def __driver():
        return ydb.Driver(
            endpoint=os.getenv("YDB_ENDPOINT"),
            database=os.getenv("YDB_DATABASE"),
            credentials=ydb.iam.ServiceAccountCredentials.from_file(
                os.getenv("SA_KEY_FILE"),
            ),
        )

    @staticmethod
    def update_state(device_id, device_state):
        attrs = {
            'device_id': device_id, 
            'device_state': device_state
        }

        with YDBContext.__driver() as driver:
            driver.wait(fail_fast=True, timeout=5)
            with ydb.SessionPool(driver) as pool:
                pool.retry_operation_sync(callee=YDBContext.__execute_update_query, **attrs)

    @staticmethod          
    def get_state(device_id):
        attrs = { 'device_id': device_id }
        
        with YDBContext.__driver() as driver:
            driver.wait(fail_fast=True, timeout=5)
            with ydb.SessionPool(driver) as pool:
                result = pool.retry_operation_sync(callee=YDBContext.__execute_select_query, **attrs)     
                if result[0].rows:
                    state = result[0].rows[0].state.decode("utf-8")
                    return ast.literal_eval(state)
                
    @staticmethod
    def __execute_update_query(session, **kwargs):
        id = bytes(kwargs['device_id'], 'utf-8') 
        state = bytes(str(kwargs['device_state']), 'utf-8')

        prepared_query = session.prepare(UPSERT_SQL)

        return session.transaction(ydb.SerializableReadWrite()).execute(prepared_query, {'$dev_id': id, '$dev_state': state }, commit_tx=True,
            settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2))
    
    @staticmethod
    def __execute_select_query(session, **kwargs):
        id = bytes(kwargs['device_id'], 'utf-8') 

        prepared_query = session.prepare(SELECT_SQL)
        return session.transaction(ydb.SerializableReadWrite()).execute(prepared_query, {'$dev_id': id }, commit_tx=True,
            settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2))