from pyModbusTCP.client import ModbusClient

import mysql.connector

import time
import datetime

db_config = {
    'database': 'prodrptdb',
    'user': 'stuser',
    'password': 'stp383',
    'host': '10.4.1.224'
}

def executesql(data, config=db_config):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    insert_stmt = (
    "INSERT INTO GFxPRoduction (Machine, Part, PerpetualCount, Timestamp)"
    "VALUES (%s, %s, %s, %s)"
    )
    
    try:
        # Executing the SQL command
        cursor.execute(insert_stmt, data)
        
        # Commit your changes in the database
        conn.commit()

    except:
        # Rolling back in case of error
        conn.rollback()

    print("Data inserted", data)
    conn.close()

def poll_count(client):

    regs = c.read_holding_registers(0, 2)
    
    if regs:
        return (regs[1]*65536)+regs[0]
        
    else:
        print("Error reaching module")
        return None

last_count = -1

# TCP auto connect on modbus request, close after it
c = ModbusClient(host="10.4.42.169", auto_open=True, auto_close=True)

while True:
    count = poll_count(c)

    if (not last_count):        # no response from unit
        pass
    elif (last_count == -1):    # first pass through
        last_count = count
    elif (count > last_count):  # one or more parts made

        for entry in range(last_count+1, count+1):
            data = ('920', '50-1467', entry, time.time())
            executesql(data)
        last_count = count

    time.sleep(2.5)

