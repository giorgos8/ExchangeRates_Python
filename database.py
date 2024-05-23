import pyodbc
import psycopg2

        
class SqlServer(object):
  
    # constructor - connection
    def __init__(self, con_str):
        connection_string = con_str
        con = pyodbc.connect(connection_string)
        self.cursor = con.cursor()
        self.cursor.fast_executemany = True
    
    
    # commit
    def commit(self):
        self.cursor.commit()

    # exececute a script
    def execute_sql_script(self, sql, commit=False):
        self.cursor.execute(sql)
        if commit == True:
            self.commit()
            
    # select one field
    def select_sql_one_value(self, sql, pos):
        result = self.cursor.execute(sql)
        for row in result:
            res = row[pos]
        return res
    
    
# inheritans
class SqlServer_ExchRates(SqlServer):
    
    def insert_exchange_rates(self, exchange_rates, coin, date):
        data = (exchange_rates['base'], coin, date, exchange_rates['rates'][coin])

        sql = f"DELETE FROM EXCHANGE_RATES WHERE FROM_CURRENCY = '{data[0]}' AND TO_CURRENCY = '{data[1]}' AND DATE = '{data[2]}'"
        self.execute_sql_script(sql, False)

        sql = f"INSERT INTO EXCHANGE_RATES (FROM_CURRENCY, TO_CURRENCY, DATE, EXCHANGE_RATE) VALUES ('{data[0]}', '{data[1]}', '{data[2]}', {data[3]})"
        self.execute_sql_script(sql, True)
                
    def write_db_trace(self, msg, info, run_aa):
        sqlExec = f"EXEC [dbo].[usp_write_trace] @INPUTMESSAGE='{msg}', @INFO='{info}', @RUNID={run_aa}"
        self.execute_sql_script(sqlExec, True)
        return True
        
    def get_next_aa(self):
        sql = f'SELECT ISNULL(MAX(trc_run_id), 0) + 1 as next_run_aa FROM traces'
        return self.select_sql_one_value(sql, 0)       
        
    def get_exchange_rate_from_db(self, date, coin):        
        sql = f"SELECT cast([EXCHANGE_RATE] as float) FROM [dbo].[EXCHANGE_RATES] WHERE [FROM_CURRENCY] = 'USD' AND [TO_CURRENCY] = '{coin}' AND [DATE] = '{date}'"
        return self.select_sql_one_value(sql, 0)
        
        
        
class PostgreSQL(object):

    # constructor - connection
    def __init__(self, psg):        
        
        con = psycopg2.connect(
            database = str(psg['database']),
            user = psg['user'],
            host = psg['host'],
            password = psg['password'],
            port = psg['port']
            )
            
        con.autocommit = True
        self.cursor = con.cursor()

    # exececute a script
    def execute_sql_script(self, sql):
        self.cursor.execute(sql)
            
    # select one field
    def select_sql_one_value(self, sql, pos):
        self.cursor.execute(sql)
        res = self.cursor.fetchone()        
        return res
        
    
# inheritans
class PostgreSQL_ExchRates(PostgreSQL):
    
    def insert_exchange_rates(self, exchange_rates, coin, date):
        data = (exchange_rates['base'], coin, date, exchange_rates['rates'][coin])

        sql = f"DELETE FROM EXCHANGE_RATES WHERE FROM_CURRENCY = '{data[0]}' AND TO_CURRENCY = '{data[1]}' AND DATE = '{data[2]}'"
        self.execute_sql_script(sql)

        sql = f"INSERT INTO EXCHANGE_RATES (FROM_CURRENCY, TO_CURRENCY, DATE, EXCHANGE_RATE) VALUES ('{data[0]}', '{data[1]}', '{data[2]}', {data[3]})"
        self.execute_sql_script(sql)
        
    def write_db_trace(self, msg, info, run_aa):        
        return True
        
    def get_next_aa(self):        
        return 1
        
    def get_exchange_rate_from_db(self, date, coin):        
        sql = f"SELECT EXCHANGE_RATE FROM EXCHANGE_RATES WHERE FROM_CURRENCY = 'USD' AND TO_CURRENCY = '{coin}' AND DATE = '{date}'"
        return self.select_sql_one_value(sql, 0)