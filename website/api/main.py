from fastapi import FastAPI, Form, Query, HTTPException
from typing import List
import ast
import re
import os
import subprocess
from datetime import date


app = FastAPI()
ALL_DATABASES: list = ["Pornhub", "Xvideos", "Xhamster"]
_ANSI_RE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def _parse_tags(stdout: str) -> dict:
    clean = _ANSI_RE.sub("", stdout).strip()
    try:
        tags = ast.literal_eval(clean)
        return tags if isinstance(tags, dict) else {}
    except (ValueError, SyntaxError):
        return {}


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/recentdata")
async def recent_data():
    "Display"
    pass


@app.get("/data/by-date/")
def data_by_date(date_str: str = Query(..., alias="date")):
    script_path: str = f"{os.path.expanduser('~')}/analyse_data.sh"
    try:
        final_date = date.fromisoformat(date_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date")

    result: subprocess.CompletedProcess = subprocess.run(
        [script_path, str(final_date), f"{ALL_DATABASES[0]}2026"],
        capture_output=True,
        text=True,
    )

    result2: subprocess.CompletedProcess = subprocess.run(
        [script_path, str(final_date), f"{ALL_DATABASES[1]}2026"],
        capture_output=True,
        text=True,
    )

    result3: subprocess.CompletedProcess = subprocess.run(
        [script_path, str(final_date), f"{ALL_DATABASES[2]}2026"],
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
async def data_range(
    items: List[str] = Form(...),
    databases: List[str] = Form(...),
):
    print("slaut")
    data = {}
    for i in items:
        print(i)
    for i in databases:
        print(i)

    return JSONResponse(data)
