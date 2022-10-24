import pymysql
import sys
import io
import configparser

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

class DBConnector :

    def __init__(self, host,port,user,pw,db) :
        self.host = host
        self.port = port
        self.user = user
        self.pw = pw
        self.db = db
        self.curs = None
    
    def connect_db (self) :
        # connect mysql 
        conn = pymysql.connect(
            host=self.host, 
            port=self.port,
            user=self.user,
            password=self.pw,
            db=self.db,
            charset='utf8')
        
        self.curs = conn.cursor()

    def execute_sql(self,sql,vars) :

        self.connect_db()

        if vars is not None :
            sql = sql.format(*vars)

        print(sql)

        # SQL execute
        self.curs.execute(sql)

        # data Fetch
        results = self.curs.fetchall()
        
        # close connection
        self.curs.close()
        return results

#TEST
"""
config = configparser.ConfigParser()
config.read('./Configuration/config.ini',encoding='utf-8-sig')
db_info = config['db']
vars = ['2020-09-27','KBO']
score_sql = config['sql']['score_sql']
connec = DBConnector(db_info['host'],int(db_info['port']),db_info['user'],db_info['pw'],db_info['db'])
results = connec.execute_sql(score_sql, vars)
print(results)
"""


