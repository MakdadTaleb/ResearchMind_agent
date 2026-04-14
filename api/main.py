from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.routes import auth, research
from api.dependencies import init_graph
from slowapi import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from api.limiter import limiter



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_graph()
    yield


api = FastAPI(
    title="ResearchMind API",
    description="AI-powered Literature Review Generator",
    version="1.0.0",
    lifespan=lifespan
)

api.state.limiter = limiter
api.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


api.include_router(auth.router)
api.include_router(research.router)
