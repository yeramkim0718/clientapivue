from Elem import *
import random

class SportsChecker :

    def __init__(self) :
        self.fake_err_dics = {}
        self.err_dics = {}

    def check_results (self,db_results, web_results) :
            
        for league in db_results :
            
            checked = 0
            games = web_results.get(league)
            db_games = db_results.get(league)
            dic = {}
            for game in games :
                if(game[WEBElem.HOME] is not None) and (game[WEBElem.AWAY] is not None) :
                    key = game[WEBElem.TIME] + game[WEBElem.HOME] + game[WEBElem.AWAY]
                    key = key.replace(" ","") 
                    dic[key] = game
        
            for db_game in db_games :
                key = db_game[DBElem.TIME] + db_game[DBElem.HOME] + db_game[DBElem.AWAY]
                key = key.replace(" ","")

                isError = False

                #Check status except 'completed'
                if db_game[DBElem.STATUS] != 'COMPLETED' :
                    print("STATUS ERROR" + str(db_game))
                    isError = True
                
                #Check score error
                if dic.get(key) is not None :
                    web_game = dic.get(key)
                    if(web_game[WEBElem.HOME_SCORE] != db_game[DBElem.HOME_SCORE]) or (web_game[WEBElem.AWAY_SCORE] != db_game[DBElem.AWAY_SCORE]) :
                        print("ERROR : SCORE DOSEN'T MATCHED")
                        print("DB : "+str(db_game))
                        print("WEB : " + str(web_game))
                        isError = True

                else :
                    print ("ERROR : There is no game in the web : " + key)
                    print(db_game)
                    isError = True
                
                if isError is False :
                    checked = checked+1
                else :
                    self.err_dics[db_game[DBElem.ID]] = db_game

            print(league + " : TOTAL : " + str(len(db_games)) + " CHECKED : " + str(checked))

    def fake_error_test (self, db_results, web_results) :

        for league in db_results :
            
            db_games = db_results.get(league)
            for i,db_game in enumerate(db_games) :
                x = random.random()

                if x < 0.05 :
                    db_game[DBElem.TIME] = '-1'
                    self.fake_err_dics[db_game[DBElem.ID]] = db_game
                if x>0.05 and x<0.1  :
                    db_game[DBElem.STATUS] = 'ABNORMAL'
                    self.fake_err_dics[db_game[DBElem.ID]] = db_game

                if x>0.1 and x<0.15:
                    db_game[DBElem.HOME_SCORE] = '-1'
                    self.fake_err_dics[db_game[DBElem.ID]] = db_game

                if x>0.15 and x <0.2 :
                    db_game[DBElem.AWAY_SCORE] = '-1'
                    self.fake_err_dics[db_game[DBElem.ID]] = db_game
                db_games[i] = db_game
            db_results[league] = db_games

        self.check_results(db_results,web_results) 

        is_same = 0
        for id in self.fake_err_dics :
            db_err = self.err_dics.get(id)
            if db_err is None :
                print("fake error dose not detected")
            else :
                is_same = is_same+1
        print("fake error : " + str(len(self.fake_err_dics)) + " same fake error game num : " +str(is_same))

