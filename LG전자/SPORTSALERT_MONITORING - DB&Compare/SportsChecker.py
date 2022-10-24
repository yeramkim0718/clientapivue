from Elem import *
from jinja2 import Environment,FileSystemLoader,Template
from collections import defaultdict
from datetime import datetime
from SportsConverter import *
from SendMail import*

class SportsChecker :

    def __init__(self, date, monitoring, web_results, score_db_results, push_db_results) :

        self.date = date
        self.monitoring = monitoring
        self.web_results = web_results
        self.score_db_results = score_db_results
        self.push_db_results = push_db_results

        self.fake_err_dics = {}
        self.score_err_dics = {}
        self.web_dic = None
        self.link_url = "https://www.flashscore.com/match/id/#match-summary/match-summary"
        self.baseball_link_url = "https://www.flashscore.com/match/id/#/match-summary/match-summary"

    def make_web_dic(self, web_results) :

        web_dic = defaultdict(dict)

        for league, games in web_results.items() :

            if league in SportsConverter.league_mapper1.keys() :
                league = SportsConverter.league_mapper1.get(league)
                print(league)

            for game in games :
                print(game)
                if(game[WEBElem.HOME] is not None) and (game[WEBElem.AWAY] is not None) :
                    key1 = (league + game[WEBElem.HOME] + game[WEBElem.AWAY]).replace(" ","")
                    key2 = game[WEBElem.TIME]                                     
                    web_dic[key1][key2] = game

        return web_dic

    def check_score_results (self,db_results, web_results) :
        
        self.db_results = db_results
        status_err = list()
        score_err = list()
        score_results = list()

        if self.web_dic is None :
            self.web_dic = self.make_web_dic(web_results)

        for league in db_results :
            
            checked = 0
            errored = 0
            db_games = db_results.get(league)
            for db_game in db_games :
                
                key1 = (league + db_game[DBElem.HOME] + db_game[DBElem.AWAY]).replace(" ","")
                key2 = db_game[DBElem.TIME]
                isError = False

                #Check status except 'completed'
                if db_game[DBElem.STATUS] != 'COMPLETED' :
                    isError = True
                    err = {}
                    err['game'] = str(db_game)
                    if key1 in self.web_dic :
                        web_games = self.web_dic.get(key1)
                        if key2 in web_games : 
                            web_game = web_games[key2]
                            web_id = web_game[WEBElem.WEBID]
                            
                            if (league == "MLB" or league == "KBO") :
                                link = self.baseball_link_url.replace("id",web_id.split("_")[2])
                            else :
                                link = self.link_url.replace("id",web_id.split("_")[2])
                            err['link'] = link
                            
                    status_err.append(err)
                    id = db_game[DBElem.ID]
                    #if id in self.push_db_results.keys() : 
                    #    del self.push_db_results[id]
                                    
                web_games = self.web_dic.get(key1)
                if web_games is None :
                    print("There is no web games in the excel list")
                    continue

                if key2 in web_games : 
                    web_game = web_games[key2]
                    if(web_game[WEBElem.HOME_SCORE] != db_game[DBElem.HOME_SCORE]) or (web_game[WEBElem.AWAY_SCORE] != db_game[DBElem.AWAY_SCORE]) :
                        isError = True
                        web_id = web_game[WEBElem.WEBID]
                        
                        if (league == "MLB" or league == "KBO") :
                            link = self.baseball_link_url.replace("id",web_id.split("_")[2])
                        else :
                            link = self.link_url.replace("id",web_id.split("_")[2])       
                                             
                        score_err.append("스코어 불일치 : " + str(db_game)+"\n" +"DB 스코어 : " + db_game[DBElem.HOME_SCORE] + " " + db_game[DBElem.AWAY_SCORE] +"<br> WEB 스코어 : " + web_game[WEBElem.HOME_SCORE] + " " + web_game[WEBElem.AWAY_SCORE]+"<br>링크 : " +link)
                else : 
                    isError = True
                    db_time = datetime.strptime(db_game[DBElem.TIME],'%Y%m%d%H%M')
                    min_time_diff = 999999
                    predicted_game = None

                    for web_time, web_game in web_games.items() :
                        web_time = datetime.strptime(web_time,'%Y%m%d%H%M')
                        time_diff = abs(db_time - web_time).total_seconds()
                        if  time_diff < min_time_diff :
                            min_time_diff = time_diff
                            predicted_game = web_game

                    if min_time_diff <= 3600 : 
                        web_id = predicted_game[WEBElem.WEBID]
                        if (league == "MLB" or league == "KBO") :
                            link = self.baseball_link_url.replace("id",web_id.split("_")[2])
                        else :
                            link = self.link_url.replace("id",web_id.split("_")[2])                               
                        
                        score_err.append("경기 시간 불일치 : " + str(db_game) +"<br>WEB 시간 : " + predicted_game[WEBElem.TIME]+"<br>링크 : " +link)

                        if(predicted_game[WEBElem.HOME_SCORE] != db_game[DBElem.HOME_SCORE]) or (predicted_game[WEBElem.AWAY_SCORE] != db_game[DBElem.AWAY_SCORE]) :
                            score_err.append("스코어 불일치 : " + str(db_game)+"<br>" +"DB 스코어 : " + db_game[DBElem.HOME_SCORE] + " " + db_game[DBElem.AWAY_SCORE] +"<br>WEB 스코어 : " + web_game[WEBElem.HOME_SCORE] + " " + web_game[WEBElem.AWAY_SCORE] +"<br>링크 : " +link)

                    else :
                        score_err.append("경기 비존재 : " + str(db_game) + "<br>")

                if isError is False :
                    checked = checked+1
                else :
                    errored = errored + 1
                    self.score_err_dics[db_game[DBElem.ID]] = db_game

            score_results.append(league + " : TOTAL : " + str(errored + checked) + " CHECKED : " + str(checked) )

        return score_results, status_err,score_err

    def check_push_results(self, web_results, push_results) :
        
        if self.web_dic is None :
            self.web_dic = self.make_web_dic(web_results)

        push_err = []
        total = len(push_results)
        error = 0

        for id,db_push in push_results.items() :
            isError = False
            key1 = (db_push[0] + db_push[2] + db_push[3]).replace(" ","")
            key2 = db_push[1]
            league = db_push[0]
            
            if key1 not in self.web_dic  :
                isError = True
                push_err.append("경기 비존재 : " + str(db_push) + "<br>")
                
            else :
                web_games = self.web_dic.get(key1)
                if key2 in web_games : 

                    web_push = self.web_dic[key1][key2]
                    web_id = web_push[WEBElem.WEBID]
                    if (league == "MLB" or league == "KBO") :
                        link = self.baseball_link_url.replace("id",web_id.split("_")[2])
                    else :
                        link = self.link_url.replace("id",web_id.split("_")[2])      
                    
                    home_push = db_push[4][0]
                    away_push = db_push[4][1]
                    web_h_push = web_push[WEBElem.PUSH][0]
                    web_a_push = web_push[WEBElem.PUSH][1]

                    for i,score in enumerate(home_push) :
                        if score == "" :
                            continue
                        score = int(score)
                        web_score = web_h_push[i]
                        if web_score != "" and web_score is not None and web_score != "X":
                            web_score = int (web_score)
                        if score != web_score :
                            isError = True

                    for i,score in enumerate(away_push) :
                        if score == "" :
                            continue

                        score = int(score)
                        web_score = web_a_push[i]
                        if web_score != "" and web_score is not None and web_score != "X":
                            web_score = int (web_score)
                        if score != web_score :
                            isError = True

                    if isError :
                        push_err.append("push 점수 불일치 : " +id +" "+ str(db_push) + "<br> web push 점수 : " + str(web_h_push) + str(web_a_push) +"<br> 링크 : " +link)
                
                else : 
                    isError = True
                    db_time = datetime.strptime(db_push[1],'%Y%m%d%H%M')
                    min_time_diff = 99999999
                    predicted_game = None

                    for web_time, web_game in web_games.items() :
                        web_time = datetime.strptime(web_time,'%Y%m%d%H%M')
                        time_diff = (db_time - web_time).total_seconds()
                        if  time_diff < min_time_diff :
                            min_time_diff = time_diff
                            predicted_game = web_game

                    if min_time_diff <= 3600 : 
                        web_id = web_game[WEBElem.WEBID]
                    
                        if league == "MLB" or league == "KBO" :
                            link = self.baseball_link_url.replace("id",web_id.split("_")[2])
                        else :
                            link = self.link_url.replace("id",web_id.split("_")[2])      
                            
                        push_err.append("경기 시간 불일치 : "  +id +" "+ str(db_push) +"<br> WEB 시간 : " + predicted_game[WEBElem.TIME]+"<br> 링크 : " +link)
                        web_push = predicted_game
                        home_push = db_push[4][0]
                        away_push = db_push[4][1]
                        web_h_push = web_push[WEBElem.PUSH][0]
                        web_a_push = web_push[WEBElem.PUSH][1]

                        push_error = False
                        for i,push in enumerate(home_push) :
                            if push == "" :
                                continue
                        
                            push = int(push)
                            web_push_ = web_h_push[i]
                            web_push_ = int (web_push_)
                            if push != web_push_ :
                                push_error = True

                        for i,push in enumerate(away_push) :
                            if push == "" :
                                continue

                            push = int(push)
                            web_push_ = web_a_push[i]
                            web_push_ = int(web_push_)
                            if push != web_push_ :
                                push_error = True

                        if push_error :
                            try :
                                push_err.append("push 점수 불일치 : " + +id +" "+ str(db_push) + "<br> web push 점수 : " + str(web_h_push) + str(web_a_push))
                            except TypeError as err :
                                print(err)

                    else :
                        push_err.append("경기 비존재 : "  +id +" "+ str(db_push) + "<br>")          

            if isError is True :
                error = error +1 

        push_results = "총 게임 수 : " + str(total) + "<br>이상 없음 : " + str(total-error) + "<br>이상 있음 : " + str(error)
        
        return push_results, push_err
        

    def check_results(self) :
        
        score_results, status_err, score_err = self.check_score_results(self.score_db_results, self.web_results)
        push_results, push_err = self.check_push_results(self.web_results, self.push_db_results)
        env = Environment(loader = FileSystemLoader('templates'))
        template = env.get_template('monitor.html')
        output = template.render(date = self.date.strftime("%Y-%m-%d") ,num = len(self.monitoring), games = sorted(self.monitoring.values(), key=lambda x : x[1]), status_err = status_err, score_results = score_results, score_err = score_err, push_err = push_err, push_results = push_results)
        
        sendMail = SendMail(self.date)
        #sendMail.send_mail(output)
        sendMail.test_send_mail(output)

        #print(self.date.strftime("%Y-%m-%d"))
        with open("./output/"+self.date.strftime("%Y-%m-%d")+".txt", "w",encoding='UTF-8') as f:
            f.write(output)
        
