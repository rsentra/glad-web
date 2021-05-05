from datetime import date, datetime,timedelta, time
 
MON, TUE, WED, THU, FRI, SAT, SUN = range(7)
HOLIDAYS2020 = ((2020,1, 1), #"new Year"
                (2020,1, 24), #"new Year"
                (2020,1, 27), #"new Year1"
                (2020,3, 1), #"3.1"
                (2020,4, 30), #"Buddha Day"
                (2020,5, 5), #"Children's Day"
                (2020,6, 6), #"Memorial Day"
                (2020,8, 15), #"Liberation Day"
                (2020,9, 30), #"Thanksgiving"
                (2020,10, 1), #"Thanksgiving1"
                (2020,10, 2), #"Thanksgiving2"
                (2020,10, 3), #"National Foundation Day"
                (2020,10, 9), #"Hangul Day"
                (2020,12, 25) #"Christmas"
                )
    
HOLIDAYS2019 = ((2019,1, 1), #"new Year"
                (2019,1, 4), #"new Year"
                (2019,1, 5), #"new Year1"
                (2019,1, 6), #"new Year2"
                (2019,3, 1), #"3.1"
                (2019,5, 6), #"Children's Day"
                (2019,6, 6), #"Memorial Day"
                (2019,8, 15), #"Liberation Day"
                (2019,9, 12), #"Thanksgiving"
                (2019,9, 13), #"Thanksgiving1"
                (2019,10, 3), #"National Foundation Day"
                (2019,10, 9), #"Hangul Day"
                (2019,12, 25) #"Christmas"
                )

def is_holiday(dt):    
        if dt.year==2020:
            HOLIDAYS = HOLIDAYS2020
        else: HOLIDAYS = HOLIDAYS2019
        if dt.weekday() >=5:
            return True
        elif (dt.year,dt.month,dt.day) in HOLIDAYS:
            return True
        else:
            return False
        
class getDateUtil():
    
    #g말일구하기
    def get_lastday(self,dt):
        next_month = lambda y, m, d: (y, m + 1, 1) if m + 1 < 13 else ( y+1 , 1, 1)
        month_end  = lambda dte: date( *next_month( *dte.timetuple()[:3] ) ) - timedelta(days=1)
        return month_end(dt)        
 
    #해당월 1일~to 사이의 영업일수
    def get_workdaysMonth(self,toDt):
        frDt=datetime(toDt.year,toDt.month,1)
#             frDt=datetime(*frDt.timetuple()[0],*frDt.timetuple()[1],1)
        workdays = (toDt - frDt).days
        for i in range(1, workdays):
            dt= frDt + timedelta(days=i)
            workdays -= is_holiday(dt)
        return workdays
    
    ## fr~to 영업일수 구하기
    def get_workdays(self,frDt,toDt):  
        workdays = (toDt - frDt).days
        for i in range(1, workdays):
            dt= frDt + timedelta(days=i)
            workdays -= is_holiday(dt)
        return workdays
    
    ##fr~to의 영업일 리스트
    def get_workdates(self,frDt,toDt):
        workdates=[]
        workdays = (toDt - frDt).days + 1
        for i in range(0, workdays):
            dt= frDt + timedelta(days=i)
            if not is_holiday(dt):
                workdates.append(dt)
        return workdates
    
        
if __name__=='__main__':
    dt=date(2020,1,1)
    getDT = getDateUtil()
    print(is_holiday(dt))
    print(getDT.get_lastday(dt))
    print(getDT.get_workdays(dt,dt+timedelta(days=30)))
    print(getDT.get_workdates(dt,dt+timedelta(days=30)))