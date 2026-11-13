# SwimCourse

Self-hosted video learning platform for swimming coaches.

## Stack
- Python / Django (server-rendered HTML)
- PostgreSQL
- Gunicorn
- Caddy (automatic HTTPS)
- Docker Compose
- Stripe Checkout and webhooks
- Private HLS media files

## Local start
1. Copy `.env.example` to `.env` and set a strong `DJANGO_SECRET_KEY`.
2. Run `docker compose up --build -d`.
3. Run `docker compose exec web python manage.py createsuperuser`.
4. Open http://localhost:8000.

For production, set `DEBUG=0`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `SITE_URL`, `CADDY_SITE`, Stripe credentials and configure HTTPS. See docs/architecture.md.

This repository is an initial implementation, not a production-ready release. Stripe subscription activation and protected video playback are not yet integrated.
