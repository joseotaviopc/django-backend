from ninja import NinjaAPI
from treinos.api import treinos_router

api = NinjaAPI()
api.add_router('', treinos_router)