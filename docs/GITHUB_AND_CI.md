# GitHub, Codespaces, and CI

Use this checklist to host the project under **[obversary-studios](https://github.com/obversary-studios)** on GitHub, keep CI green, and show the full engineering story: clone → Codespace → Compose → Actions → future deploy hooks.

## 1. Create the repository

1. On GitHub, create a new repository under the org **Obversary Studios** (`obversary-studios`).  
   - Suggested name: `memory-dropbox` (or match your naming convention).  
   - Do **not** add a README, `.gitignore`, or license if you already have them locally (avoids merge noise).

2. From your machine (any terminal with `git` and SSH or HTTPS):

```bash
cd /path/to/memory-dropbox
git remote add origin git@github.com:obversary-studios/memory-dropbox.git
# or: https://github.com/obversary-studios/memory-dropbox.git

git branch -M main   # optional: rename master → main to match GitHub default
git push -u origin master   # or: git push -u origin main
```

## 2. Confirm CI

- Open **Actions** on the repo; the **CI** workflow should run on every push and PR to `main` / `master`.  
- Jobs: **lint** (Ruff + byte-compile) and **compose** (`docker compose config`).

## 3. GitHub Codespaces

- **Code → Codespaces → Create codespace** on the default branch.  
- The devcontainer installs Python dev deps and enables Docker-in-Docker so you can run:

```bash
cp .env.example .env   # if not already present
docker compose up --build
```

- Use the **Ports** tab to open the forwarded UI/API (port `8000`).

**Note:** Local Compose uses `network_mode: host` for the API service; if anything behaves oddly in Codespaces, prefer validating with `docker compose config` and adjust networking in a follow-up for cloud environments.

## 4. Showing “the whole process” (optional next steps)

| Piece | Purpose |
|--------|--------|
| **Branch protection** | Require PR + passing **CI** before merge to `main`. |
| **Environments** | `staging` / `production` with approval gates if you add deploy jobs later. |
| **Deploy workflow** | Second workflow on `workflow_dispatch` or `release` that builds images and pushes to GHCR. |
| **Webhooks** | Notify external systems (e.g. deploy pipeline, Slack) on push or release. |
| **Org secrets** | Registry tokens, kubeconfigs, or API keys — never commit them. |

## 5. Webhooks (overview)

**Settings → Webhooks → Add webhook**: choose payload URL, content type `application/json`, events (e.g. **Push**, **Pull requests**, **Releases**). Use this when you want an external runner or PaaS to react to this repo without polling.

---

This file is the operational companion to the product roadmap: same repo, same progression story, visible on GitHub.
