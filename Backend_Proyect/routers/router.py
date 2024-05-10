from fastapi import APIRouter


router = APIRouter(prefix='/', tags=["API"] , responses={404:{"mesege": "No encontrado"} })



@router.get('/')
async def use_root():
    return {"Hola":"Mundo"}


@router.post('/')
async def reload():
    return


@router.delete('/')
async def delete():
    return