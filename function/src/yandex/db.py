from os import environ as env
import ydb
import ydb.iam
import ast

UPSERT_SQL = """
DECLARE $capability_id AS String;
DECLARE $device_id AS String;
DECLARE $device_state AS String;

UPSERT INTO device_capability_states (key, device_id, state) 
VALUES ($capability_id, $device_id, $device_state);"""

SELECT_SQL = """
DECLARE $capability_id AS String;

SELECT state FROM device_capability_states WHERE key = $capability_id;
"""

class YDBContext:
    @staticmethod
    def __driver():
        return ydb.Driver(
            endpoint=env.get("YDB_ENDPOINT"),
            database=env.get("YDB_DATABASE"),
            credentials=ydb.iam.MetadataUrlCredentials(),
        )
        

    @staticmethod
    def update_state(capability_id, device_id, device_state):
        attrs = {
            'capability_id': capability_id,
            'device_id': device_id, 
            'device_state': device_state
        }

        with YDBContext.__driver() as driver:
            driver.wait(fail_fast=True, timeout=5)
            with ydb.SessionPool(driver) as pool:
                pool.retry_operation_sync(callee=YDBContext.__execute_update_query, **attrs)

    @staticmethod          
    def get_state(capability_id):
        attrs = { 'capability_id': capability_id }
        
        with YDBContext.__driver() as driver:
            driver.wait(fail_fast=True, timeout=5)
            with ydb.SessionPool(driver) as pool:
                result = pool.retry_operation_sync(callee=YDBContext.__execute_select_query, **attrs)     
                if result[0].rows:
                    state = result[0].rows[0].state.decode("utf-8")
                    return ast.literal_eval(state)
                
        return None
                
    @staticmethod
    def __execute_update_query(session, **kwargs):
        id = bytes(kwargs['capability_id'], 'utf-8') 
        device_id = bytes(kwargs['device_id'], 'utf-8') 
        state = bytes(str(kwargs['device_state']), 'utf-8')

        prepared_query = session.prepare(UPSERT_SQL)

        return session.transaction(ydb.SerializableReadWrite()).execute(prepared_query, {
                '$capability_id': id, 
                '$device_id': device_id,
                '$device_state': state 
            }, commit_tx=True,
            settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2))
    
    @staticmethod
    def __execute_select_query(session, **kwargs):
        id = bytes(kwargs['capability_id'], 'utf-8') 

        prepared_query = session.prepare(SELECT_SQL)
        return session.transaction(ydb.SerializableReadWrite()).execute(prepared_query, {'$capability_id': id }, commit_tx=True,
            settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2))