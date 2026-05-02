import ast
import re
from datetime import date, timedelta
import os
import mariadb
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import subprocess


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")  # type: ignore


def index2(request):
    return render(request, "website/index.html")


def donate(request):
    return render(request, "website/donate.html")


def analyse(request):
    today = date.today()
    days = [today - timedelta(days=i) for i in range(5)]
    return render(request, "website/analyse.html", {"days": days})


def ressource(request):
    return render(request, "website/ressource.html")


def thoughts(request):
    return render(request, "website/thoughts.html")


ALL_DATABASES: list = ["Pornhub", "Xvideos", "Xhamster"]


_ANSI_RE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def zzzzzzzzzzzzzzzzdata_by_date(request):
    date_str = request.GET.get("date", "")
    script_path: str = f"{os.path.expanduser('~')}/analyse_data.sh"
    try:
        final_date = date.fromisoformat(date_str)
    except ValueError:
        return JsonResponse({"error": "Invalid date"}, status=400)

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

    return JsonResponse(
        {
            "databases": {
                ALL_DATABASES[0]: parse_tags(result.stdout),
                ALL_DATABASES[1]: parse_tags(result2.stdout),
                ALL_DATABASES[2]: parse_tags(result3.stdout),
            }
        }
    )
