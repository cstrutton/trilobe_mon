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
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Executing the SQL command
        cursor.execute(insert_stmt, data)
        print(now, " Data inserted", data)
        
        # Commit your changes in the database
        conn.commit()

    except:
        # Rolling back in case of error
        conn.rollback()
        print(dt, " Data insert failed", data)

    conn.close()

def poll_count(client):

    regs = c.read_holding_registers(16, 4)

    di8 = regs[0] + (regs[1]*65536)
    di9 = regs[2] + (regs[3]*65536)
    
    if regs:
        return di8, di9
        
    else:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now, " Error reaching module")
        time.sleep(20)
        return None, None

last_count8 = -1
last_count9 = -1

# TCP auto connect on modbus request, close after it
c = ModbusClient(host="10.4.42.169", auto_open=True, auto_close=True, timeout=5)

while True:
    count8, count9 = poll_count(c)

    if (not count8):        # no response from unit
        pass
    elif (last_count8 == -1):    # first pass through
        last_count8 = count8
        last_count9 = count9
    if (count8 > last_count8):  # one or more parts made on left arm
        for entry in range(last_count8+1, count8+1):
            data = ('650L', '50-1467', entry, time.time())
            executesql(data)
        last_count8 = count8
    if (count9 > last_count9):  # one or more parts made on left arm
        for entry in range(last_count9+1, count9+1):
            data = ('650R', '50-1467', entry, time.time())
            executesql(data)
        last_count9 = count9

    time.sleep(2.5)

