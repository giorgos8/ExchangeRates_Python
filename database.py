import pyodbc

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

        sql = f"DELETE FROM [dbo].[EXCHANGE_RATES] WHERE [FROM_CURRENCY] = '{data[0]}' AND [TO_CURRENCY] = '{data[1]}' AND [DATE] = '{data[2]}'"
        self.execute_sql_script(sql, False)

        sql = f"INSERT INTO [dbo].[EXCHANGE_RATES] ([FROM_CURRENCY], [TO_CURRENCY], [DATE], [EXCHANGE_RATE]) VALUES ('{data[0]}', '{data[1]}', '{data[2]}', {data[3]})"
        self.execute_sql_script(sql, True)
                
    def write_db_trace(self, msg, info, run_aa):
        sqlExec = f"EXEC [dbo].[usp_write_trace] @INPUTMESSAGE='{msg}', @INFO='{info}', @RUNID={run_aa}"
        self.execute_sql_script(sqlExec, True)
        return True
        
    def get_next_aa(self):
        sql = f'select [dbo].[SFN_GET_NEXT_AA]() as next_run_aa'
        return self.select_sql_one_value(sql, 0)       
        
    def get_exchange_rate_from_db(self, date, coin):        
        sql = f"SELECT [EXCHANGE_RATE] FROM [dbo].[EXCHANGE_RATES] WHERE [FROM_CURRENCY] = 'USD' AND [TO_CURRENCY] = '{coin}' AND [DATE] = '{date}'"
        return self.select_sql_one_value(sql, 0)