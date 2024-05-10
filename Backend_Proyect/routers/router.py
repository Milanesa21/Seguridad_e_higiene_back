from fastapi import APIRouter


router = APIRouter(prefix='/home', tags=['Api'])



@router.get('/')
async def use_root():
    return {"Hola":"Mundo"}


@router.post('/')
async def reload():
    return


@router.delete('/')
async def delete():
    return