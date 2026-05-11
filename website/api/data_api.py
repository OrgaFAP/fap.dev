from http.client import FAILED_DEPENDENCY
from rich import print
from datetime import datetime
from website.api.connect_db import Analyse_Database
import mariadb
import pandas as pd

ALL_DATABASES: tuple = ("Xvideos2026", "Xhamster2026", "Pornhub2026")


class Query_API(Analyse_Database):
    "Handle all API Call"

    def __init__(self, data: dict) -> None:
        super().__init__()
        self.data: dict = data

    def query_data_range(self) -> str:
        "Format the SQL Query"

        query: str = f"""
        SELECT title,link,date,tags FROM january WHERE date >= '{self.data["date"][0]}' AND date <= '{self.data["date"][1]}'
            UNION ALL SELECT title,link,date,tags FROM february WHERE date >= '{self.data["date"][0]}' AND date <= '{self.data["date"][1]}'
            UNION ALL SELECT title,link,date,tags FROM march WHERE date >= '{self.data["date"][0]}' AND date <= '{self.data["date"][1]}'
            UNION ALL SELECT title,link,date,tags FROM april WHERE date >= '{self.data["date"][0]}' AND date <= '{self.data["date"][1]}'
            UNION ALL SELECT title,link,date,tags FROM may WHERE date >= '{self.data["date"][0]}' AND date <= '{self.data["date"][1]}'
            UNION ALL SELECT title,link,date,tags FROM june WHERE date >= '{self.data["date"][0]}' AND date <= '{self.data["date"][1]}'
            UNION ALL SELECT title,link,date,tags FROM july WHERE date >= '{self.data["date"][0]}' AND date <= '{self.data["date"][1]}'
            UNION ALL SELECT title,link,date,tags FROM august WHERE date >= '{self.data["date"][0]}' AND date <= '{self.data["date"][1]}'
            UNION ALL SELECT title,link,date,tags FROM september WHERE date >= '{self.data["date"][0]}' AND date <= '{self.data["date"][1]}'
            UNION ALL SELECT title,link,date,tags FROM october WHERE date >= '{self.data["date"][0]}' AND date <= '{self.data["date"][1]}'
            UNION ALL SELECT title,link,date,tags FROM november WHERE date >= '{self.data["date"][0]}' AND date <= '{self.data["date"][1]}'
            UNION ALL SELECT title,link,date,tags FROM december WHERE date >= '{self.data["date"][0]}' AND date <= '{self.data["date"][1]}';
        """
        print(query)

        return query

    def check_date(self):
        "Check and convert to format DATETIME"

        dates: list[str] = self.data["date"]
        self.dates_data_range: list[str] = []
        try:
            for i in dates:
                self.dates_data_range.append(
                    datetime.fromisoformat(i).strftime("%Y-%m-%d 00:00:00")
                )  # type: ingore

            print("[+] Dates OK")
            return True
        except ValueError:
            print("Bad input")
            return False

    def check_date_database(self):
        "Check if the Database is correct"
        date_data_range: tuple = self.data["sources"]

        for db in date_data_range:
            if db in ALL_DATABASES:
                ...
            else:
                print("bad")
                return False
        print("[+] Databases OK")
        return True

    def check_api_data_range(self) -> bool:
        "API /data/range"

        self.result_data_range: list[tuple] = []
        # Check INPUT user
        if self.check_date_database() is True and self.check_date() is True:
            query: str = self.query_data_range()
            for db in self.data["sources"]:
                context_db: mariadb.Connection = self._connect(db)
                data: list[tuple] = self.execute_query(context_db, query)
                for i in data:
                    self.result_data_range.append(i)
        return True

    def export_csv(self) -> str | bool:
        "Export STDOUT into a .CSV file"

        try:
            filename: str = f"/tmp/fap_dev_{self.data['date'][0].replace('00:00:00', '')}-{self.data['date'][1].replace('00:00:00', '')}".strip().replace(
                " ", ""
            )
            filename = filename + ".csv"
            df: pd.DataFrame = pd.DataFrame(
                self.result_data_range, columns=["TITLE", "LINK", "DATE", "TAGS"]
            )
            print(df)
            df.to_csv(filename, index=True)

            return filename
        except Exception as e:
            print("Error while export .CSV : ", e)
            return False
