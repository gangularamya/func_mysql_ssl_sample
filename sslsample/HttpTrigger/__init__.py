import logging

import azure.functions as func
import pathlib
import mysql.connector
from mysql.connector import errorcode


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:

        conn = mysql.connector.connect(
        user='username@pythonfuncmysqldb', 
        password='xxxxx', 
        host='pythonfuncmysqldb.mysql.database.azure.com', 
        port=3306, 
        database='functestdb',
        ssl_ca=get_ssl_cert()
            )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.info("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logging.info("Database does not exist")
        else:
            logging.info(err)
    else:
        cursor = conn.cursor()
        # Drop previous table of same name if one exists
        cursor.execute("DROP TABLE IF EXISTS inventory;")
        logging.info("Finished dropping table (if existed).")

        # Create table
        cursor.execute("CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity VARCHAR(50));")
        logging.info("Finished creating table.")

        # Cleanup
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Done.")

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )

def get_ssl_cert():
    current_path = pathlib.Path(__file__).parent.parent
    return str(current_path / 'BaltimoreCyberTrustRoot.crt.pem')        
