from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.users.router import router2 as router_users2
from app.hotels.router import router as router_hotels
from app.pages.router import router as router_pages
from fastapi.staticfiles import StaticFiles
from app.static.images.router import router as router_images
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from redis import asyncio as aioredis
from fastapi_cache.backends.redis import RedisBackend
from app.config import setting


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{setting.REDIS_HOST}:{setting.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache:")
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Access-Control-Allow-Origins", "Authorization"],
)

app.mount("/static", StaticFiles(directory="app/static"), "static")
app.include_router(router_bookings)
app.include_router(router_images)
app.include_router(router_pages)
app.include_router(router_users)
app.include_router(router_users2)
app.include_router(router_hotels)