from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config.setting import Settings

settings = Settings()

celery_engine = create_async_engine(
    url=settings.db_url,
    echo=True,
    poolclass=NullPool,
)

CelerySessionFactory = async_sessionmaker(
    bind=celery_engine,
    autoflush=False,
    expire_on_commit=False,
)