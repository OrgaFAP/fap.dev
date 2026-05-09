from os import environ
import mariadb
from rich import print
import warnings
from scrap.globals import (
    get_month,
    get_yesterday,
    convert_month,
)
import argparse
import json
from datetime import datetime
import re


class Query_API:
    "Handle all API Call"

    def query_data_range(self, range_date: list[str]) -> str:
        "Format the SQL Query"

        print(range_date)

        query: str = f"""
        SELECT * FROM january WHERE date >= '{range_date[0]}' AND date <= ''
            UNION ALL SELECT * FROM february WHERE date >= '{range_date[0]}' AND date <= '{range_date[1]}'
            UNION ALL SELECT * FROM march WHERE date >= '{range_date[0]}' AND date <= '{range_date[1]}'
            UNION ALL SELECT * FROM april WHERE date >= '{range_date[0]}' AND date <= '{range_date[1]}'
            UNION ALL SELECT * FROM may WHERE date >= '{range_date[0]}' AND date <= '{range_date[1]}'
            UNION ALL SELECT * FROM june WHERE date >= '{range_date[0]}' AND date <= '{range_date[1]}'
            UNION ALL SELECT * FROM july WHERE date >= '{range_date[0]}' AND date <= '{range_date[1]}'
            UNION ALL SELECT * FROM august WHERE date >= '{range_date[0]}' AND date <= '{range_date[1]}'
            UNION ALL SELECT * FROM september WHERE date >= '{range_date[0]}' AND date <= '{range_date[1]}'
            UNION ALL SELECT * FROM october WHERE date >= '{range_date[0]}' AND date <= '{range_date[1]}'
            UNION ALL SELECT * FROM november WHERE date >= '{range_date[0]}' AND date <= '{range_date[1]}'
            UNION ALL SELECT * FROM december WHERE date >= '{range_date[0]}' AND date <= '{range_date[1]}';
        """

        return query

    def check_api_data_range(self, dates: list) -> list[str]:
        "API /data/range"

        dates_data_range: list[str] = []
        try:
            for i in dates:
                dates_data_range.append(
                    datetime.fromisoformat(i).strftime("%Y-%m-%d 00:00:00")
                )  # type: ingore

            return dates_data_range

        except ValueError:
            print("Bad input")
            exit(1)
