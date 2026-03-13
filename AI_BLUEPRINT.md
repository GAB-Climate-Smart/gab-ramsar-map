# GAB FARMS ERP & MRV SYSTEM - MASTER BLUEPRINT
**CRITICAL INSTRUCTION:** You are a senior Next.js and Supabase developer. You MUST read this file before executing any task, planning any sprint, or writing any code.

## 1. PROJECT CONTEXT & STACK
- **Project:** Agricultural ERP and Blue Carbon MRV (Measurement, Reporting, and Verification) system.
- **Core Stack:** Next.js (App Router), Supabase Pro (PostgreSQL + PostGIS), Vercel SDK (AI), Mapbox GL JS, Tailwind CSS, shadcn/ui.
- **Goal:** Tier 3 scientific data accuracy, secure cloud deployment, and strict Human-in-the-Loop (HITL) data entry.

## 2. DYNAMIC ARCHITECTURE CHECK (AVOID AMNESIA)
- Do NOT assume you know what is already built.
- Before proposing new UI components or routing, you MUST use the terminal to run `ls -la app/` and `ls -la components/` to dynamically check the existing directory structure.
- Never duplicate existing modules (e.g., Soil Lab, Map Views).

## 3. THE CLI WORKFLOW
We use a strict CLI stack for all infrastructure. Use these tools via the terminal:
- **Database:** `npx supabase` (for migrations, type generation, starting local studio). All database calls must use the Supabase Server Client.
- **Hosting:** `vercel` (e.g., `vercel dev`, `vercel env pull`).
- **Version Control:** `gh` (GitHub CLI) and standard `git` commands.

## 4. SECRETS & AUTHENTICATION (STRICT RULE)
- **NEVER** ask the user for API keys, passwords, or tokens.
- **NEVER** hardcode keys into components or scripts.
- All secrets (Supabase URL, Anon Key, Mapbox Token, etc.) live strictly in the `.env.local` file. Read from `process.env` only.

## 5. THE END OF SHIFT PROTOCOL (CI/CD)
You are not finished with a task until the code is safely in the cloud. Upon completing any approved feature, you must autonomously execute:
1. `git status`
2. `git add .`
3. `git commit -m "feat/fix: [brief description]"`
4. `git push origin main`
