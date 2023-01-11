from database.base_connection import Session
from database.models.tables import User
from fastapi import APIRouter

api_user_router = APIRouter()


@api_user_router.get("/get_websites_list_user/{user_id}")
async def get_websites_list_user(user_id: int):
    # TODO ensure that the user making the request is authorized
    with Session() as session:
        user = session.get(User, user_id)  # Get User using id
        websites_association_table = user.websites
        websites = [web.website for web in websites_association_table]
    return websites
