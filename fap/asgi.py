import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fap.settings')

from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from django.core.asgi import get_asgi_application
from starlette.routing import Mount
from starlette.applications import Starlette

django_app = ASGIStaticFilesHandler(get_asgi_application())

from website.api.main import app as fastapi_app

application = Starlette(routes=[
    Mount('/api', app=fastapi_app),
    Mount('', app=django_app),
])
