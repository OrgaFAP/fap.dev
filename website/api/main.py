from fastapi import FastAPI, Form, Query, HTTPException, Request
from typing import List
import ast
import re
import os
import subprocess
from datetime import date
from website.api.data_api import Query_API

app: FastAPI = FastAPI()
ALL_DATABASES: list = ["Pornhub", "Xvideos", "Xhamster"]
_ANSI_RE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/data/by-date/")
async def data_by_date(date_str: str = Query(..., alias="date")):
    try:
        final_date = date.fromisoformat(date_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date")

    result: subprocess.CompletedProcess = subprocess.run(
        ["website/api/analyse_data.sh", str(final_date), f"{ALL_DATABASES[0]}2026"],
        capture_output=True,
        text=True,
    )
    result2: subprocess.CompletedProcess = subprocess.run(
        ["website/api/analyse_data.sh", str(final_date), f"{ALL_DATABASES[1]}2026"],
        capture_output=True,
        text=True,
    )

    result3: subprocess.CompletedProcess = subprocess.run(
        ["website/api/analyse_data.sh", str(final_date), f"{ALL_DATABASES[2]}2026"],
        capture_output=True,
        text=True,
    )

    def parse_tags(stdout: str) -> dict:
        clean = _ANSI_RE.sub("", stdout).strip()
        try:
            tags = ast.literal_eval(clean)
            return tags if isinstance(tags, dict) else {}
        except (ValueError, SyntaxError):
            return {}

    print(parse_tags(result.stdout))
    return {
        "databases": {
            ALL_DATABASES[0]: parse_tags(result.stdout),
            ALL_DATABASES[1]: parse_tags(result2.stdout),
            ALL_DATABASES[2]: parse_tags(result3.stdout),
        }
    }


@app.post("/data/range/")
async def data_range(request: Request):
    payload: dict = await request.json()
    print(payload)
    qa_api: Query_API = Query_API(payload)
    if qa_api.check_api_data_range() is True:
        qa_api.export_csv()
