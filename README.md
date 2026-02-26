uv run alembic -c src/alembic.ini revision --autogenerate -m "message"
uv run alembic -c src/alembic.ini upgrade head
docker compose --env-file .db.env up