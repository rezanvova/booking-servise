import os
from fastapi import FastAPI,APIRouter
from app.bookings.router import router as router_bookings
from app.users.router import router2 as router_users2
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.pages.router import router as  router_pages
app = FastAPI()

app.include_router(router_bookings)
app.include_router(router_pages)
app.include_router(router_users)
app.include_router(router_users2)
app.include_router(router_hotels)
