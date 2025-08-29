from fastapi import FastAPI
from routers.category_router import router as category_router
from routers.product_router import router as product_router

app = FastAPI()


app.include_router(category_router)
app.include_router(product_router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
