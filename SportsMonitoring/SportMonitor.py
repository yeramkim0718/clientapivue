import sys
import io
import os
from apscheduler.schedulers.background import BackgroundScheduler 
import time
from datetime import datetime, timedelta
from SeleniumCrawler import*
from DBConnector import*
from SportsScoreConverter import*
from SportsChecker import*

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

class SportsMonitor (SeleniumCrawler) :

    def __init__(self, browser,config_path,date) :
        SeleniumCrawler.__init__(self,browser)

        self.date = datetime.strptime(date,"%Y-%m-%d")
        self.db_oldest_dates = {}

        self.config = configparser.ConfigParser()
        self.config.optionxform = str
        self.config.read(config_path,encoding='utf-8-sig')

        self.comple_log = configparser.ConfigParser()
        self.comple_log.optionxform = str
        self.comple_path = self.config['info']['comple_path']
        self.comple_log.read(self.comple_path,encoding = 'utf-8-sig')

        self.n_comple_log = configparser.ConfigParser()
        self.n_comple_log.optionxform = str
        self.n_comple_path = self.config['info']['n_comple_path']
        self.n_comple_log.read(self.n_comple_path,encoding = 'utf-8-sig')

        self.more_tag = self.config['info']['more_tag']
        self.league2Url = self.config['url']
        self.url2League = {}
        for url, league in zip(self.league2Url.values(),self.league2Url.keys()) :
            self.url2League[url] = league
        self.sportsmapper = self.config['sport_ids']

        self.score_leagues = set(self.config['info']['score_leagues'].split(","))
        self.push_leagues = set(self.config['info']['push_leagues'].split(","))
        self.crawle_leagues =  self.score_leagues | self.push_leagues
        self.crawle_info = {} # key : url, value : list of tags (0 : score_tags, 1 : push_tags)

        self.monitoring = {} #key : id, value : game info
        self.nextmonitoring = {} #key : id, value : game info
        self.db_results = {} # key : id, value : game info
        self.push_db_results = {} #key : id, value : game pushes
        
        self.web_results = {} # 
        self.push_web_results = {} # 

        self.converter = SportsScoreConverter()

        self.score_sql = self.config['sql']['score_sql']
        self.push_sql = self.config['sql']['push_days_sql']
        
        self.prefs = self.config._sections.get('prefs')
        self.arguments = [*self.config._sections.get('argument')]

        db_info = self.config['db']
        self.db_host = db_info['host']
        self.db_port = int(db_info['port'])
        self.db_user = db_info['user']
        self.db_pw = db_info['pw']
        self.def_db = db_info['db']

    def check_whether_montiroing(self, game_push) :

        starttime = datetime.strptime(game_push[-1][PushElem.START_TIME],"%Y%m%d%H%M")
        endtime = datetime.strptime(game_push[-1][PushElem.LOG_TIME], "%Y%m%d%H%M")
        end_status = game_push[-1][PushElem.STATUS]
        id = game_push[0][PushElem.ID]

        self.push_db_results[id] = game_push

        if starttime >= self.date and endtime < self.date + timedelta(days = 1) and end_status != 'IN_PROGRESS' :
            self.monitoring[id] = (game_push)[-1]

        if starttime>=self.date and endtime >= self.date + timedelta(days=1):
            self.nextmonitoring[id] = (game_push)[-1]


    def record_monitoring_log(self) :
        date = self.date.strftime("%m%d")
        
        print("monitoring")
        for id, game in self.monitoring.items() :
            print(game)

        print("next monitoring")
        for game in self.nextmonitoring.values() :
            print(game)

        with open (self.comple_path, 'w+', encoding='UTF-8') as file :
            self.comple_log[date] = {}
            for id,game in self.monitoring.items() :
                self.comple_log.set(date,id,str(game))
            self.comple_log.write(file)

        with open (self.n_comple_path, 'w+', encoding='UTF-8') as file :
            self.n_comple_log[date] = {}
            for id,game in self.nextmonitoring.items() :
                tmp = ""
                for elem in game :
                    tmp = tmp + elem + ","
                tmp = tmp[:-1]

                self.n_comple_log.set(date,id,tmp)
            self.n_comple_log.write(file)
        
    def split_game_push(self, results) :

        game_push = []
        b_id = results[0][PushElem.ID]
        id = -1

        for result in results :
            sport_id = result[PushElem.SPORT_ID]
            if self.sportsmapper[sport_id] is None :
                continue

            id = result[PushElem.ID]
            if id != b_id :
                if len(game_push) > 0 :                    
                    #n_results[b_id] = game_push
                    self.check_whether_montiroing(game_push)
                    game_push = []

            game_push.append(result)
            b_id = id

        self.check_whether_montiroing(game_push)

        yesterday = (self.date - timedelta(days = 1)).strftime("%m%d")
        
        ids = {}

        if yesterday in self.n_comple_log : 
            ids = self.n_comple_log[yesterday]
        
        for id in ids : 
            game = self.n_comple_log[yesterday][id]
            self.monitoring[id] = game

        self.record_monitoring_log()

    def get_push_list_from_db(self) :

        connec = DBConnector(self.db_host,self.db_port,self.db_user,self.db_pw,self.def_db)
        yesterday = (self.date - timedelta(days=1)).strftime('%Y-%m-%d')

        sql = self.push_sql

        vars = [yesterday, self.date.strftime("%Y-%m-%d")]

        results = connec.execute_sql(sql, vars)        
        self.split_game_push(results)

    def u_get_score_list_from_db (self,date,league) :

        connec = DBConnector(self.db_host,self.db_port,self.db_user,self.db_pw,self.def_db)
        vars = [date,date,league]

        results = connec.execute_sql(self.score_sql, vars)
        return results

    def set_db_oldest_dates(self, league) :

        oldest_idx = len(self.db_results[league])-1
        oldest_date = self.db_results[league][oldest_idx][DBElem.TIME]

        if self.db_oldest_dates.get(league) is None :
            self.db_oldest_dates[league]  = oldest_date

        if self.db_oldest_dates.get(league)  > oldest_date :
            self.db_oldest_dates[league] = oldest_date

    def print_monitoring_data(self) :
        print("Monitoring data list")
        print(self.date)
        for game in self.monitoring.values() :
            print(game)

    def get_score_list_from_db(self) :
        
        for league in self.crawle_leagues :
            date = self.date.strftime("%Y-%m-%d")
            db_results_per_league = self.u_get_score_list_from_db(date,league)
            
            if len(db_results_per_league) > 0  :
                self.db_results[league] = db_results_per_league
                self.set_db_oldest_dates(league)
        
        self.print_monitoring_data()

    # setting to gmt time+0
    def set_gmt_zero (self) :  
        try :          
            self.driver.find_element_by_css_selector('.header__button.header__button--settings').click()
            self.driver.find_element_by_id('tzactual-icon').click()
            self.driver.find_element_by_xpath('//*[@id="tzcontent"]/li[contains(.,"GMT+0")]').click()
            self.driver.implicitly_wait(1)
            self.driver.find_element_by_xpath('//*[@id="lsid-window-close"]').click()
        except StaleElementReferenceException as e :
            print(e.msg)
            self.driver.find_element_by_xpath('//*[@id="tzcontent"]/li[contains(.,"GMT+0")]').click()
            self.driver.implicitly_wait(1)
            self.driver.find_element_by_xpath('//*[@id="lsid-window-close"]').click()
            
    def check_crawle_dates(self, league, s_result, push_result,parser) :
        
        try :
            dates = s_result[WEBElem.TIME]
            oldest_idx = len(dates) -1
            oldest_web_date = dates[oldest_idx]
            oldest_web_date = self.converter.change_web_time_format(oldest_web_date)

            """if int(self.db_oldest_dates[league]) < int(oldest_web_date) :
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.1)
                self.driver.find_element_by_xpath(self.more_tag).click()
                time.sleep(1)
                s_tags = self.config['score_tags'][league].split(",")
                s_result = self.parse(parser,s_tags)
                push_tags = self.config['push_tags'][league].split(",")
                push_result = self.parse(parser,push_tags)
            """
            
            return s_result,push_result

        except :
            return

    #make crawle_info  (self.crawle_info) = {} # key : url, value : list of tags (0 : total tag, 1: score_tags, 2 : push_tags)
    def make_crawle_info(self) :

        """if len (self.monitoring) == 0 :
            return {}

        leagues = set([])
        for game in self.monitoring.values():
            league = game[PushElem.LEAGUE]
            leagues.add(league)
        
        self.crawle_leagues = (self.crawle_leagues & leagues)  
        """
        
        for league in self.crawle_leagues :
            url = self.league2Url.get(league)
            score_tags = []
            push_tags = []
            if league in self.config['score_tags'] :
                score_tags = self.config['score_tags'][league].split(",")
            if league in self.config['push_tags'] :
                push_tags = self.config['push_tags'][league].split(",")
            if league in self.config['total_tag'] :
                total_tag = self.config['total_tag'][league]

            self.crawle_info[url] = [total_tag,score_tags, push_tags]

    def make_game_list (self,soup, total_tag, score_tags, push_tags) :
        list = soup.select(total_tag)
        
        score_list = []
        push_list = []

        for html in list :
            txts = []
            for tag in score_tags :
                txt = html.select_one(tag)
                txt = txt.get_text().replace("\xa0","")
                txts.append(txt)
            score_list.append(txts)

            txts = []
            for tag in push_tags :
                txt = html.select_one(tag)
                if txt is None :
                    txt = ""
                else :
                    txt = txt.get_text().replace("\xa0","")
                txts.append(txt)
            push_list.append(txts)
        return score_list, push_list
        
    def crawleAndParse (self,parser) :
        self.set_options(self.prefs, self.arguments)
        self.load_webdriver()

        first = True

        for url, tag_list in self.crawle_info.items() :
            
            total_tag = tag_list[0]
            score_tags = tag_list[1]
            push_tags = tag_list[2]
            
            self.driver.get(url)

            if first is True :
                self.set_gmt_zero()
                first = False

            #from this, parsing part
            page = self.driver.page_source
            soup = BeautifulSoup(page, features = "lxml")
            score_list, push_list = self.make_game_list(soup,total_tag, score_tags, push_tags)

            league = self.url2League.get(url)
            
            #score_result,push_result = self.check_crawle_dates(league,score_result,push_result,parser)

            self.web_results[league] = score_list
            self.push_web_results[league] = push_list

        self.quit_webdriver()
        return self.web_results,self.push_web_results

    def change_format (self) :
        self.web_results = self.converter.change_web_format(self.web_results)
        #self.db_results = self.converter.change_db_format(self.db_results)
        return self.web_results, self.db_results

    def get_web_results(self,parser) :
        self.make_crawle_info()
        self.crawleAndParse(parser)
        
        for league,push_results in self.push_web_results.items() :
            print(league)
            for i,result in enumerate(push_results) :
                print(str(i) + str(self.web_results[league][i]) + str(result))

"""def monitoring () :
    
    config_path = './Configuration/config.ini'    

    dates = ['2020-11-20','2020-11-21','2020-11-22','2020-11-23','2020-11-24','2020-11-25']
#    dates.append((datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d'))
    sm = SportsMonitor(SeleniumCrawler.Driver.CHROME,config_path)
    sm.get_completed_list_from_db(dates)
    sm.get_web_results('html.parser')
    sm.change_format()
    checker = SportsChecker()
    checker.check_results(sm.db_results, sm.web_results)
 #   checker.fake_error_test(sm.db_results, sm.web_results)"""

def test_push_monitoring() :
    config_path = './Configuration/config.ini'    
    date = '2020-11-25'
    sm = SportsMonitor(SeleniumCrawler.Driver.CHROME,config_path,date)
    #sm.get_push_list_from_db()
    #sm.get_score_list_from_db()
    sm.get_web_results('html.parser')
    sm.change_format()

test_push_monitoring()
"""
sched = BackgroundScheduler()
sched.add_job(monitoring, 'cron', hour = '21',minute="47", id="schdeuler_test")
sched.start()

while True :
    print(".")
    time.sleep(1)
"""

#monitoring()
"""
config_path = './Configuration/config.ini'    
dates = ['2020-10-12']
sm = SportsMonitor(SeleniumCrawler.Driver.CHROME,config_path)
sm.get_push_list_from_db(dates)
"""