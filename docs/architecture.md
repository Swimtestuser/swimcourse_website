# SwimCourse architecture (ADR-001)

## Goals
Subscription video library for swimming coaches with 20-30 initial videos, filters by swim style and equipment, favorites and a simple admin interface.

## Decisions
- Modular Django monolith with server-side templates, minimal JavaScript, PostgreSQL.
- Docker Compose on a Hetzner VPS, Caddy for HTTPS.
- Stripe-hosted Checkout and Customer Portal for recurring payments; signed and idempotent webhooks are required before activating subscriptions.
- Private video assets on a non-public volume, transcoded offline with FFmpeg to HLS. Do not expose raw MP4s or playlists.
- Playback authorization must be enforced on **every** HLS playlist, segment and encryption-key request using a short-lived signed playback session tied to an authenticated, entitled user. A public static media route is forbidden.
- HLS and short-lived signed sessions reduce casual unauthorized sharing but cannot prevent authorized users from downloading content using tools like yt-dlp. Stronger protection would require managed DRM (Widevine/FairPlay) and a compatible player.
- No React, Redis, Celery or microservices for the MVP.

## Domain
User, Subscription, SwimStyle, Equipment, Exercise, VideoAsset, Favorite, and StripeWebhookEvent. Exercises can reference multiple equipment items. Favorite must be unique per user and exercise.

## Security requirements
CSRF and secure session cookies, password hashing, verified email before purchase, throttling of authentication endpoints, admin-only uploads, size/type limits, non-public originals, encrypted backups, structured logs, secret management, verified Stripe webhook signatures, replay-safe events, access checks at media delivery.

## MVP sequence
1. Project scaffold, models, Django admin, registration/login.
2. Exercise list, swim-style/equipment filters, favorites.
3. Stripe checkout, customer portal, verified webhooks, subscription authorization.
4. Offline HLS conversion, protected segment delivery and player.
5. Tests, backup/restore, HTTPS hardening, privacy/legal review.

## Operations
Use pinned dependencies and Docker image tags, regular security updates, daily PostgreSQL and media backups, restore tests, log rotation and uptime monitoring. Store all secrets outside Git.
