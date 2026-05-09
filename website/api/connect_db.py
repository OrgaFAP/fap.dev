from os import environ
import mariadb
from rich import print
import warnings
import argparse
import json
from datetime import datetime
import re
from website.api.globals import (
    get_month,
    get_yesterday,
    get_month_number,
    convert_month,
)

warnings.filterwarnings("ignore", category=SyntaxWarning)
LIMIT_TAGS = 20


class Analyse_Database:
    "Database object related"

    def __init__(self) -> None:
        "Init some variables"
        super().__init__()
        self.databases: tuple = ("Xvideos2026", "Xhamster2026", "Pornhub2026")

    def _connect(self, site: str):
        "Connect to the Mariadb server and Database"

        try:
            conn: mariadb.Connection = mariadb.connect(
                user="user_study",
                password=f"{environ['DB_PASSWORD']}",
                host="localhost",
                database=f"{site}",
            )

            return conn

        except Exception as e:
            print(e)
            exit(1)

    def _get_today(self) -> str:
        "SQL Query for today"

        today: str = f"SELECT * FROM {get_month()} WHERE date = CURDATE();"
        print(today)
        return today

    def _get_yesterday(self) -> str:
        "SQL Query for yesterday"
        yesterday: str = get_yesterday()
        sql_query: str = (
            f"SELECT * FROM {get_month()} WHERE DATE(date) = '{yesterday} 00:00:00';"
        )
        print(sql_query)

        return sql_query

    def _get_week(self) -> str:
        "SQL Query for the week"

        sql_query: str = (
            f"SELECT * FROM {get_month()} WHERE date >= NOW() - INTERVAL 7 DAY;"
        )
        print(sql_query)

        return sql_query

    def all_tags_in_one_list(self, query_response: list) -> list:
        "Get every tags from sql query into an unique list"

        big_list: list = []
        for x in query_response:
            to_list: list = json.loads(x[4])
            for x in to_list:
                big_list.append(x)

        return big_list

    def sanitize_tags(self, all_tags: dict) -> dict:
        "Remove all useless tags (like HDVideos, nude etc ...)"

        useless_tag: list = [
            "HD Porn",
            "4K Porn",
            "HDPorn",
            "Pornstar",
            "Verified Amateurs",
            "VerifiedAmateurs",
            "Exclusive",
            "sexy",
            "60FPS",
            "© 2007 - 2025, xHamster.com",
            "JavaScript is required for this website. Please turn it on in your browser and reload the page",
            "FapHouse",
            "HDVideos",
            "Nude",
        ]
        for _ in useless_tag:
            all_tags.pop(_, None)

        return all_tags

    def five_most_tags(self, data: list) -> dict:
        "Display the 5 most reccurent tags"

        data_dict: dict = {}
        # Index at 1 by default
        for tag in data:
            if tag not in data_dict.keys():
                data_dict.update({tag: 1})
            else:
                data_dict.update({tag: data_dict[tag] + 1})

        data_dict: dict = dict(
            sorted(data_dict.items(), key=lambda x: x[1], reverse=True)
        )
        data_dict = self.sanitize_tags(data_dict)

        count: int = 0
        final_dict: dict = {}  # Contain 5-10 tags
        for tag in data_dict.items():
            final_dict.update({tag[0]: tag[1]})
            count += 1
            if count == LIMIT_TAGS:
                break

        print(final_dict)
        return final_dict

    def _get_year(self) -> str:
        "SQL Query for the entire year"

        sql_query: str = """SELECT * FROM january 
        UNION ALL SELECT * FROM february 
        UNION ALL SELECT * FROM march 
        UNION ALL SELECT * FROM april 
        UNION ALL SELECT * FROM may 
        UNION ALL SELECT * FROM june 
        UNION ALL SELECT * FROM july 
        UNION ALL SELECT * FROM august 
        UNION ALL SELECT * FROM september 
        UNION ALL SELECT * FROM october 
        UNION ALL SELECT * FROM november 
        UNION ALL SELECT * FROM december;"""

        return sql_query

    def _get_month(self) -> str:
        "SQL Query for the entire month"

        query: str = f"SELECT * FROM {get_month()};"

        return query

    def execute_query(self, context: mariadb.Connection, sql_query: str) -> list:
        "Execute SQL command"

        # query -> list[0] -> tuple(str)
        conn: mariadb.Connection = context
        cursor = conn.cursor()
        # sql_query = f"SELECT tags FROM {get_month()}"
        cursor.execute(sql_query)
        query_response: list = cursor.fetchall()

        if len(query_response) == 0:
            print("[+] Empty Set !")

        conn.commit()
        conn.close()

        return query_response

    def check_input_data(self, input: str) -> bool:
        "Check input from /api/"

        pattern: re.Pattern = re.compile(r"^\d{4}\-\d{2}-\d{2}$")
        if pattern.match(input):
            number_month: str = slice(5, 7)  # type: ignore
            month_nb: str = input[number_month]  # type: ignore
            month_lt: str = convert_month(month=month_nb)
            self.month_lt = month_lt

            return True

        return False

    def main(self) -> None: ...


if __name__ == "__main__":
    x: Analyse_Database = Analyse_Database()
    x.main()
