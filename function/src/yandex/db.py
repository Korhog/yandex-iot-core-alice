# Yandex DB integration test
from dotenv import load_dotenv
load_dotenv()

import os
import ydb
import ydb.iam

def execute_query(session):
    return session.transaction().execute(
        "select 1 as cnt;",
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2),
    )


def main():
    driver = ydb.Driver(
        endpoint=os.getenv("YDB_ENDPOINT"),
        database=os.getenv("YDB_DATABASE"),
        credentials=ydb.iam.ServiceAccountCredentials.from_file(
            os.getenv("SA_KEY_FILE"),
        ),
    )

    with driver:
        driver.wait(fail_fast=True, timeout=5)
        with ydb.SessionPool(driver) as pool:
            result = pool.retry_operation_sync(execute_query)
            assert result[0].rows[0].cnt == 1

main()