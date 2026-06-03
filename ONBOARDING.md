# Onboarding Guide

Welcome to the wiki! This guide walks you through everything you need to set up your environment and start contributing, even if you've never used Git or GitHub before.

## What You Need

1. **A GitHub account** — for submitting your contributions
2. **GitHub Desktop** (free) — for syncing changes with the team, no terminal needed
3. **Obsidian** (free) — for browsing and reading the wiki
4. **An AI assistant** — Claude Code, Cursor, Copilot, or similar

## Step 1: Create a GitHub Account

1. Go to [github.com/signup](https://github.com/signup)
2. Enter your email address and click **Continue**
3. Create a password (at least 15 characters, or 8 characters with a number and lowercase letter)
4. Choose a username — this is your public identity on GitHub (e.g. `anna-schmidt`). Keep it short and recognisable. You can't easily change it later.
5. Complete the email verification — GitHub sends a code to your email, enter it on the page
6. Choose the **Free** plan (it has everything you need)
7. You can skip the personalisation questions if you like

Your username is what the project maintainer needs to give you access. Send it to them and wait for the invitation — you'll receive an email from GitHub asking you to accept access to the repository.

## Step 2: Install GitHub Desktop

1. Download [GitHub Desktop](https://desktop.github.com/) and install it
2. Open GitHub Desktop and sign in with your GitHub account
3. That's it — GitHub Desktop handles authentication automatically, no SSH keys or passwords to configure

## Step 3: Clone the Repository

This downloads the wiki to your computer.

1. In GitHub Desktop: **File** > **Clone repository**
2. Find `larsgson/wiki-llm` in the list (it appears once the maintainer has given you access), or paste the URL: `https://github.com/larsgson/wiki-llm`
3. Choose where to save it on your computer (remember this location — you'll need it for Obsidian)
4. Click **Clone**

You now have a local copy of the entire wiki.

## Step 4: Open in Obsidian

1. Download and install [Obsidian](https://obsidian.md/)
2. Open Obsidian and choose **Open folder as vault**
3. Select the `wiki-llm` folder you just cloned
4. Browse the wiki starting from `wiki/index.md`

## Step 5: Set Up Your AI Assistant

The wiki conventions are defined in `CLAUDE.md`. Your AI assistant needs to follow these rules.

- **Claude Code:** reads `CLAUDE.md` automatically — no extra setup needed
- **Cursor / Copilot / other tools:** paste the contents of `CLAUDE.md` into your AI tool at the start of each session, or configure it as a system prompt

## How to Contribute

You never edit `main` directly. Instead, you work on your own branch and submit a pull request (PR) for review. GitHub Desktop makes this straightforward.

### 1. Create a branch for your work

1. In GitHub Desktop, make sure **Current branch** (top bar) says `main`
2. Click **Current branch** > **New branch**
3. Name it `yourname/topic-description` (e.g. `anna/add-water-governance-sources`)
4. Click **Create branch**

You're now working on your own branch. All changes happen here, separate from `main`.

### 2. Do your work

Use your AI assistant to ingest sources or update pages. The AI will create and edit files in the `wiki/` folder on your computer.

Before fetching any external URL, check `wiki/source-registry.md` to make sure it hasn't already been processed.

### 3. Review and commit your changes

After your AI assistant has made changes:

1. Open GitHub Desktop — it automatically detects all changed files
2. In the left panel, review the list of changed files. Click any file to see what changed (green = added, red = removed)
3. Check the boxes next to the files you want to include
4. At the bottom left, write a short summary of what you changed (e.g. "Add water governance sources and update index")
5. Click **Commit to yourname/topic-description**

You can commit multiple times on your branch — think of each commit as a checkpoint.

### 4. Push your branch to GitHub

After committing, click **Publish branch** (first time) or **Push origin** (subsequent pushes) in the top bar. This uploads your branch to GitHub.

### 5. Open a pull request

1. After pushing, GitHub Desktop shows a banner: **Create Pull Request** — click it
2. This opens GitHub in your browser with the PR template pre-filled
3. Go through the checklist in the template (conventions followed, source registry updated, etc.)
4. Click **Create pull request**
5. Wait for a reviewer to approve, then it gets merged into `main`

### 6. Stay up to date with main

Before starting new work, get the latest changes:

1. In GitHub Desktop: switch to `main` using the **Current branch** dropdown
2. Click **Fetch origin** in the top bar, then **Pull origin** if there are new changes
3. Create a new branch from the updated `main` (step 1 above)

## Key Rules to Remember

1. **Never push directly to `main`** — always use a branch and PR
2. **Check the source registry** before fetching any URL — avoid duplicate work
3. **Never modify files in `raw/`** — they are immutable source material
4. **Never copy external content verbatim** — only AI-generated summaries with source URLs
5. **Feed `CLAUDE.md` to your AI tool** — it contains all the conventions

## Getting Help

- Read `CLAUDE.md` for all wiki conventions and workflows
- Read `ROADMAP.md` for the project plan
- Check `wiki/index.md` to see what already exists
- Ask the project maintainer if you get stuck

---

## Alternative: Command Line

If you prefer working in a terminal instead of GitHub Desktop, here's the equivalent workflow.

### One-time setup

Install Git:
- **Windows:** Download [Git for Windows](https://git-scm.com/download/win), use default settings. This gives you "Git Bash".
- **Mac:** Run `xcode-select --install` in Terminal.

Set up SSH keys (so GitHub knows it's you):
1. `ssh-keygen -t ed25519 -C "your-email@example.com"` — press Enter for defaults
2. Copy your public key:
   - **Mac:** `pbcopy < ~/.ssh/id_ed25519.pub`
   - **Windows (Git Bash):** `cat ~/.ssh/id_ed25519.pub` then select and copy
3. On GitHub: profile picture > **Settings** > **SSH and GPG keys** > **New SSH key** > paste and save
4. Test: `ssh -T git@github.com`

Clone the repo:
```
git clone git@github.com:larsgson/wiki-llm.git
cd wiki-llm
```

### Contributing via terminal

| What you want to do | Command |
|---------------------|---------|
| See what branch you're on | `git branch` |
| Switch to main | `git checkout main` |
| Pull latest changes | `git pull` |
| Create a new branch | `git checkout -b yourname/topic` |
| See what's changed | `git status` |
| Stage wiki changes | `git add wiki/` |
| Stage a new source file | `git add raw/your-file.docx` |
| Commit staged changes | `git commit -m "your message"` |
| Push to GitHub (first time) | `git push -u origin yourname/topic` |
| Push to GitHub (after first time) | `git push` |

After pushing, open a pull request on [github.com/larsgson/wiki-llm](https://github.com/larsgson/wiki-llm).
