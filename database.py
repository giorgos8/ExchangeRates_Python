import pyodbc

class SqlServer(object):
  
    def __init__(self, con_str):
        connection_string = con_str
        con = pyodbc.connect(connection_string)

        self.cursor = con.cursor()
        self.cursor.fast_executemany = True

    def commit(self):
        self.cursor.commit()

    
    def insert_exchange_rates(self, exchange_rates, coin, date):
        data = (exchange_rates['base'], coin, date, exchange_rates['rates'][coin])        

        sqlDelete = f"DELETE FROM [dbo].[EXCHANGE_RATES] WHERE [FROM_CURRENCY] = '{data[0]}' AND [TO_CURRENCY] = '{data[1]}' AND [DATE] = '{data[2]}'"
        #print(sqlDelete)
        self.cursor.execute(sqlDelete)

        sqlInsert = f"INSERT INTO [dbo].[EXCHANGE_RATES] ([FROM_CURRENCY], [TO_CURRENCY], [DATE], [EXCHANGE_RATE]) VALUES ('{data[0]}', '{data[1]}', '{data[2]}', {data[3]})"
        #print(sqlInsert)
        self.cursor.execute(sqlInsert)
        
        self.commit()
        
    def get_exchange_rate_from_db(self, date, coin):        
        result = self.cursor.execute(f"SELECT [EXCHANGE_RATE] FROM [dbo].[EXCHANGE_RATES] WHERE [FROM_CURRENCY] = 'USD' AND [TO_CURRENCY] = '{coin}' AND [DATE] = '{date}'")
        for row in result:
            res = row.EXCHANGE_RATE
        return res
    
    def get_next_aa(self):
        result = self.cursor.execute(f'select [dbo].[fnGetNextRunID]() as next_run_aa')
        for row in result:
            res = row.next_run_aa
        return res
        
    def write_db_trace(self, msg, info, run_aa):
        self.cursor.execute(f"EXEC [dbo].[usp_write_trace] @INPUTMESSAGE=?, @INFO=?, @RUNID=?", msg, info, run_aa)
        self.commit()
        return True