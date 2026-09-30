# Deployment Guide

ResumeLens is a monorepo. The FastAPI backend is deployed as a Render Web
Service, and the Vite frontend is deployed as a Vercel project. Both are linked
to the GitHub repository's `main` branch so production updates can follow a
normal commit-and-push workflow.

## Render backend

The repository-root `render.yaml` describes the backend service:

- Runtime: native Python (no Docker)
- Branch: `main`
- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check: `/health`
- Automatic deployment: on each commit to the linked branch
- Python runtime: `3.13.15`

To create it, sign in to Render, connect the GitHub repository, and create a
Blueprint from the repository's `render.yaml`. The first preview can run without
`DATABASE_URL`: `/health` and the API's basic routes do not require PostgreSQL,
but `/health/database` will report unavailable until Supabase is connected.
After creating the Vercel project, set `CORS_ORIGINS` in the Render dashboard
to the exact Vercel production origin. Do not put database credentials or other
secrets in `render.yaml` or Git.

The `free` plan is suitable for an early preview and may spin down when idle.
The Render service listens on the platform-provided `$PORT`; it must bind to
`0.0.0.0` so Render can route traffic to it.

## Production PostgreSQL

Create the production database in Supabase. In the Supabase dashboard, use
**Connect** to obtain the PostgreSQL connection string. For an IPv4-only
backend, Supabase documents its shared session pooler as the connection option;
copy its host, port, and username from the dashboard instead of constructing
them manually. Keep the full string private and add it as Render's
`DATABASE_URL` environment variable. Percent-encode reserved password
characters before storing the URL.

After configuring the production database, apply the committed Alembic
migrations using the production connection before enabling database-dependent
features. Add the production URL as Render's `DATABASE_URL` environment
variable. Do not use the local database URL in Render. Keep the connection
string private and never paste it into chat or commit it.

## Vercel frontend

In Vercel, import the same GitHub repository as a separate project and set:

- Framework preset: Vite
- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`
- Production branch: `main`
- Environment variable: `VITE_API_BASE_URL=https://<your-render-service>.onrender.com`

Set `VITE_API_BASE_URL` for the Production environment. It is a public API URL,
not a secret. Do not put `DATABASE_URL`, `GEMINI_API_KEY`, or `JWT_SECRET` in
Vercel variables prefixed with `VITE_`.

Vercel's Git integration creates deployments from the connected repository;
confirm that `main` is selected as the production branch. When the Vercel URL
is available, add its exact origin to Render's `CORS_ORIGINS`, save the Render
environment change, and verify the API from the deployed site.

## Prove automatic deployment

After the first successful deployment, make a harmless UI text change, run
`npm run build` locally, commit and push it to `main`, then confirm that Vercel
builds the new frontend commit. A backend-only change should trigger Render's
service build as well. A Render Blueprint with a backend `rootDir` may skip
deploys for commits that do not affect files under `backend/`.

## Official references

- [Render FastAPI deployment](https://render.com/docs/deploy-fastapi)
- [Render monorepo support](https://render.com/docs/monorepo-support)
- [Render automatic deploys](https://render.com/docs/deploys)
- [Render Blueprint reference](https://render.com/docs/blueprint-spec)
- [Vercel monorepos](https://vercel.com/docs/monorepos)
- [Vercel Git deployments](https://vercel.com/docs/git)
- [Supabase PostgreSQL connections](https://supabase.com/docs/guides/database/connecting-to-postgres)
