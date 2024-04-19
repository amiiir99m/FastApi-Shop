from fastapi import FastAPI
import uvicorn
from db.engine import Base, engine
from routers.users import router as user_router
from routers.categories import router as category_router
from routers.products import router as product_router
from routers.images import router as image_router
from routers.carts import router as cart_router


from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

#@app.on_event("startup")
#async def init_tables():
#    async with engine.begin() as conn:
#        await conn.run_sync(Base.metadata.create_all)
#if you don't want to work with sqlalchemy active this code


app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(category_router, prefix="/category", tags=["category"]) 
app.include_router(product_router, prefix="/products", tags=["products"]) 
app.include_router(image_router, prefix="/images", tags=["images"]) 
app.include_router(cart_router, prefix="/carts", tags=["carts"]) 




if __name__ == "__main__":
    uvicorn.run(app)
