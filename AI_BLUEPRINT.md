# GAB CLIMATE SMART — MASTER AI BLUEPRINT
**CRITICAL INSTRUCTION:** You are a senior Next.js and Supabase developer working for GAB Climate Smart Investment Ltd. You MUST read this entire file before executing any task, planning any sprint, or writing any code.

---

## 1. PROJECT CONTEXT & STACK
- **Organisation:** GAB Climate Smart Investment Ltd — Ghanaian agribusiness (farm, agribusiness, consultancy, land divisions)
- **Projects:** GAB OS (company dashboard), GAB Farms ERP (farm operations), Blue Carbon MRV, GAB Ramsar Map
- **Core Stack:** Next.js (App Router), Supabase Pro (PostgreSQL + PostGIS), Vercel (hosting + AI SDK), Mapbox GL JS, Tailwind CSS, shadcn/ui
- **Goal:** Tier 3 scientific data accuracy, secure cloud deployment, and strict Human-in-the-Loop (HITL) data entry

---

## 2. DYNAMIC ARCHITECTURE CHECK (AVOID AMNESIA)
- Do NOT assume you know what is already built.
- Before proposing new UI components or routes, run `ls -la app/` and `ls -la components/` to check the existing structure.
- Never duplicate existing modules (e.g., Soil Lab, Map Views, Farm Agent).

---

## 3. ENVIRONMENT BOOTSTRAP — READ THIS BEFORE WRITING ANY CODE

### Step 1 — Pull all app secrets from Vercel (single source of truth)
All project secrets (Supabase URLs, API keys, Mapbox token, etc.) live in Vercel Environment Variables.
Run this from inside the project directory to get a local `.env.local`:
```bash
vercel env pull .env.local
```
This requires the Vercel CLI to be authenticated (see Step 2). Never hardcode keys. Never ask the user for keys.

### Step 2 — Authenticate the CLI tools

#### Vercel CLI
- **Local (macOS):** Auth token is stored at `~/Library/Application Support/com.vercel.cli/auth.json`
- **Cloud / CI agents:** Set the `VERCEL_TOKEN` environment variable. The team ID is `team_lo3ulbRrV03KJe87XF043ftU`.
- **Check:** `vercel whoami`
- **If not authenticated:** `vercel login` (browser flow) or set `VERCEL_TOKEN`

#### Supabase CLI
- **Usage:** Always use `npx supabase` (not a global install) — current version: 2.78.1
- **Cloud / CI agents:** Set the `SUPABASE_ACCESS_TOKEN` environment variable (get from Supabase dashboard → Account → Access Tokens)
- **Check:** `npx supabase projects list`
- **If not authenticated:** `npx supabase login` or set `SUPABASE_ACCESS_TOKEN`

#### GitHub CLI
- **Local (macOS):** Token stored in macOS keychain under `gh:github.com` (user: `bustabus48-lab`)
- **Cloud / CI agents:** Set the `GH_TOKEN` environment variable
- **Check:** `gh auth status`
- **If not authenticated:** `gh auth login` or set `GH_TOKEN`
- **Note:** `gh` may not be globally installed — install with `brew install gh` if missing

### Step 3 — Verify your environment
After pulling `.env.local`, confirm these keys are present before writing any data code:
```
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY
ERP_SUPABASE_URL
ERP_SUPABASE_SERVICE_ROLE_KEY
NEXT_PUBLIC_MAPBOX_TOKEN
```

---

## 4. TWO-DATABASE ARCHITECTURE
This project uses TWO Supabase projects — never confuse them:

| | GAB OS | Farm ERP |
|---|---|---|
| **Purpose** | Company OS: finance, alerts, projects, consultancy | Source of truth for all farm data |
| **Client var** | `NEXT_PUBLIC_SUPABASE_URL` | `ERP_SUPABASE_URL` |
| **Usage** | `createClient()` from `@/lib/supabase` | `erpAdminClient()` from `@/lib/erpClient` |
| **Owns** | transactions, alerts, buyers, projects | blocks, produce_lots, tasks, inputs, block_metrics |

---

## 5. CLI WORKFLOW
Use these tools via the terminal for all infrastructure work:
- **Database migrations:** `npx supabase db push` or run SQL in Supabase Dashboard SQL Editor
- **Type generation:** `npx supabase gen types typescript --project-id <id> > types/database.ts`
- **Local dev:** `vercel dev` (pulls env vars automatically)
- **Env sync:** `vercel env pull .env.local`
- **Deploy:** `git push origin main` (Vercel auto-deploys on push to main)

---

## 6. SECRETS POLICY (STRICT)
- **NEVER** hardcode API keys, tokens, or passwords anywhere in code
- **NEVER** commit `.env.local` to git (it is in `.gitignore`)
- **NEVER** ask the user for keys — always pull them from Vercel or read from `process.env`
- All secrets flow: Vercel Dashboard → `vercel env pull` → `.env.local` → `process.env`

---

## 7. END OF SHIFT PROTOCOL (CI/CD)
You are not finished until the code is in the cloud. After any approved feature:
```bash
git status
git add .
git commit -m "feat/fix: [brief description]"
git push origin main
```
Vercel auto-deploys on push to `main`. Confirm the deployment succeeded at vercel.com/dashboard.
