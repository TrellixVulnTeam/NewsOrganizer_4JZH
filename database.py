from typing import List

import mysql.connector as mysql

from news.article import NewsSite, Country
from utils.singleton import Singleton


class DatabaseConnector(metaclass=Singleton):
    def __init__(self):
        self.__database = mysql.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='news'
        )
        self.__cursor = self.__database.cursor()

    def get_countries(self) -> List[Country]:
        query = 'SELECT * FROM countries'
        self.__cursor.execute(query)

        return [Country(name, code) for _, name, code in self.__cursor.fetchall()]

    def get_news_sites(self, country: str) -> List[NewsSite]:
        query = 'SELECT news_sites.name, news_sites.code, countries.name FROM news_sites INNER JOIN countries ON ' \
                'news_sites.country_id = countries.id WHERE countries.code = %s'
        self.__cursor.execute(query, (country,))

        return [NewsSite(site_name, code, country_name) for site_name, code, country_name in self.__cursor.fetchall()]
