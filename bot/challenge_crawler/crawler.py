import requests
import os, re
import json
from bs4 import BeautifulSoup
import sqlite3

# REGEX PATTERN
PATTERN = {
    'date' : r"(\d+\. ?\d+\. ?\d+ ?(\(.\))?)"
}

DEBUG = True

class CrawlerDB:
    ''' 크롤러 '''
    database_file_name = "crawl.db"
    
    _code_file_path    = os.path.realpath(__file__) 
    _workspace_dir     = _code_file_path.split('/bot/')[0]
    _database_dir      = _workspace_dir + '/db/'

    database_path      = _database_dir + database_file_name
    connection         = sqlite3.connect(database_path)
    db                 = connection.cursor()

    table_name = 'challenge_notices'

    def __init__(self): 
        try:
            self.db.execute('SELECT count(*) FROM {} limit 1'.format(self.table_name))
        except sqlite3.OperationalError:
            if DEBUG:
                print("*** Table not found. Creating...")
            create_query = """
                CREATE TABLE {}(
                    target_name   TEXT,
                    title         TEXT,
                    datetime      TEXT,
                    is_notice     INTEGER
                )""".format(self.table_name)
            try:
                self.db.execute(create_query)
                self.connection.commit()
            except:
                self.connection.rollback()

    def insert(self, notice_list):
        new_notice_list = []
        for notice in notice_list:
            query = "SELECT * FROM {} WHERE target_name=? AND title=?".format(self.table_name)
            self.db.execute(query, (notice['target_name'], notice['title']))

            result = self.db.fetchall()
            if len(result) == 0:
                new_notice_list.append((
                    notice['target_name'],
                    notice['title'],
                    notice['datetime'],
                    0,
                ))
        
        query = "INSERT INTO {} VALUES(?, ?, ?, ?)".format(self.table_name)
        
        try:
            self.db.executemany(query, new_notice_list)
            self.connection.commit()
        except:
            self.connection.rollback()

        return

    

class NhsukCrawler(CrawlerDB):
    '''
    (주) 한국우주기술개발산업
        - RC-CAR 메이커 경진 대회
    '''
    name       = "한국우주기술개발산업"
    sub_name   = "RC-CAR 메이커 경진대회"
    url = "https://nhsuk.creatorlink.net/"

    def update(self):
        response = requests.get(self.url)
        parsed_data = self._parse(response.text)
        
        notice_list = []
        for data in parsed_data:
            notice_list.append({
                'target_name' : self.name,
                'title'       : data['title'],
                'datetime'    : data['datetime'],
            })

        self.insert(notice_list)

        if DEBUG:
            for notice in parsed_data:
                print("*" * 50)
                print("id            : ", notice['id'])
                print("title         : ", notice['title'])
                print("category_name : ", notice['category_name'])
                print("datetime      : ", notice['datetime'])
            
        return

    def _parse(self, html_code):
        match = re.search(r"CONTENTS : (\{.*\}),", html_code)

        data = json.loads(match.group(1))
        notice_data = data["el10344329"]

        notice_list = notice_data['list']['list']
        notice_list.reverse()

        return notice_list



class KookminUnivCrawler(CrawlerDB):
    '''
    국민대학교
        - 국민대 자율주행 경진대회
    '''
    name       = "국민대학교"
    sub_name   = "국민대학교 자율주행 경진대회"
    url = "https://auto-contest.kookmin.ac.kr"
    
    def update(self):
        response = requests.get(self.url)
        parsed_data = self._parse(response.text)
        
        notice_list = [{
            'target_name' : self.name,
            'title'       : parsed_data['title'],
            'datetime'    : parsed_data['참가접수'],
        }]

        self.insert(notice_list)
        

        if DEBUG:
            print("*" * 50)
            print('대회명            : ', parsed_data['title'])
            print('참가접수          : ', parsed_data['참가접수'])
            print('예선설명회        : ', parsed_data['예선설명회'])
            print('예선 과제 수행    : ', parsed_data['예선과제수행'])
            print('본선 진출팀 발표  : ', parsed_data['본선진출팀발표'])
            print('본선설명회        : ', parsed_data['본선설명회'])
            print('대회준비 시험주행 : ', parsed_data['대회준비시험주행'])
            print('본선 대회         : ', parsed_data['본선대회'])

        return

    def _parse(self, html_code):
        soup = BeautifulSoup(html_code, 'html.parser')
        competition_title = soup.select_one('header a > span').get_text()

        data = {}
        data['title'] = competition_title
        for h3 in soup.select('h3'):
            match = re.search(r"(.{2,10}) +" + PATTERN['date'], h3.get_text())
            if match:
                info_name = match.group(1).strip().replace(' ', '')
                data[info_name] = match.group(2)

        return data


class LgeRobotContestCrawler(CrawlerDB):
    '''
    LG전자 로봇 인큐베이션 공모전
    '''
    name       = "LG전자 로봇"
    sub_name   = "로봇 인큐베이션 공모전"
    url = "https://lge-robot-contest.com/information"

    def update(self):
        response = requests.get(self.url)
        data = self._parse(response.text)
        
        response = requests.get(self.url)
        parsed_data = self._parse(response.text)
        
        notice_list = [{
            'target_name' : self.name,
            'title'       : parsed_data['title'],
            'datetime'    : parsed_data['지원서접수'],
        }]

        self.insert(notice_list)

        if DEBUG:
            print("*" * 50)
            print('대회명             : ', parsed_data['title'])
            print('지원서 접수        : ', parsed_data['지원서접수'])
            print('서류심사           : ', parsed_data['서류심사'])
            print('면접심사           : ', parsed_data['면접심사'])
            print('본선 진출자 발표   : ', parsed_data['본선진출자발표'])
            print('본선 프로젝트 진행 : ', parsed_data['본선프로젝트진행'])
            print('최종 공모전 심사   : ', parsed_data['최종공모전심사'])

        return

    def _parse(self, html_code):
        soup = BeautifulSoup(html_code, 'html.parser')

        data = {}
        data['title'] = soup.select_one('header a.logo-img').get_text()
        for li in soup.select('.contents-day-box li'):
            span_list = li.select('span')
            if span_list:
                info_name = span_list[0].get_text().strip().replace(' ', '')
                value = span_list[1].get_text()
                data[info_name] = value

        return data

class KiroCrawler(CrawlerDB):
    '''
    한국로봇융합연구원
        - 국방로봇경진대회
    '''
    name       = "한국로봇융합연구원"
    sub_name   = "국방로봇경진대회"
    url = "http://kiro.re.kr/alert/notice.asp"

    def update(self):
        response = requests.get(self.url)
        response.encoding='EUC-KR'
        parsed_data = self._parse(response.text)

        notice_list = []
        for data in parsed_data:
            notice_list.append({
                'target_name' : self.name,
                'title'       : data[2],
                'datetime'    : data[3],
            })

        self.insert(notice_list)

        # print
        if DEBUG:
            for d in parsed_data:
                print("*" * 50)
                print('no       : ', d[0])
                print('category : ', d[1])
                print('title    : ', d[2])
                print('date     : ', d[3])

    def _parse(self, html_code):
        soup = BeautifulSoup(html_code, 'html.parser')
        tr_list = soup.select('.container table tbody tr')

        data = []
        for tr in tr_list:
            td_list = tr.select('td')
            no       = td_list[0].get_text()
            category = td_list[1].get_text()
            title    = td_list[2].select_one('a')['title']
            date     = td_list[4].get_text()
            data.append((no, category, title, date))

        return data

if __name__ == '__main__':
    nhsuk   = NhsukCrawler()
    nhsuk.update()
    
    kookmin = KookminUnivCrawler()
    kookmin.update()
    
    lgerb   = LgeRobotContestCrawler()
    lgerb.update()

    kiro    = KiroCrawler()
    kiro.update()




