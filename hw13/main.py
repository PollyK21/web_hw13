from fastapi import FastAPI
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from hw11.routes import contacts, auth, users
from hw11.conf.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [ 
    "http://localhost:3000"
    ]

app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    """
    This function is called when the application starts up.
    It initializes the Redis connection and sets up rate limiting.
    """
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)

@app.get("/")
def read_root():
    """
    A simple root endpoint that returns a welcome message.
    """
    return {"message": "Hello World"}
