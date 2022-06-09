from fastapi import APIRouter

site_router = APIRouter(prefix='/site')


@site_router.get('/')
async def site_route():
    return {'msg': 'site'}