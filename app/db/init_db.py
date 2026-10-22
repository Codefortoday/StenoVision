from app.core.config import settings
from app.crud import user as user_crud
from app.db.session import Base, SessionLocal, engine
from app.models.user import Role


def init_db() -> None:
    import app.models  # noqa: F401  (registers tables with Base)

    Base.metadata.create_all(bind=engine)

    # Create the first admin from .env, otherwise nobody could assign roles.
    if settings.FIRST_ADMIN_EMAIL and settings.FIRST_ADMIN_PASSWORD:
        with SessionLocal() as db:
            if not user_crud.get_by_email(db, settings.FIRST_ADMIN_EMAIL):
                user_crud.create_user(
                    db,
                    email=settings.FIRST_ADMIN_EMAIL,
                    full_name="System Admin",
                    password=settings.FIRST_ADMIN_PASSWORD,
                    role=Role.ADMIN,
                )