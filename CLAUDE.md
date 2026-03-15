# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<!-- BEGIN: .agents/rules/docker.md -->
# File Editing vs Execution
- **Reading and editing existing files** (Read, Edit tools): Do these directly on the host — no Docker needed.
- **Creating new files**: MUST go through the Docker sandbox. **NEVER use the Write tool to create files** — it runs on the host and bypasses the sandbox.
  - **Recommended pattern for files with complex content**: (1) Create a stub file via Docker: `docker compose run --rm sandbox bash -c "echo '# stub' > //workspace/path/to/file"`, then (2) use the Edit tool on the host to fill in the content (editing existing files on the host is allowed). This avoids bash heredoc escaping issues that are common in Git Bash on Windows.
  - **For short/simple files**: Use `docker compose run --rm sandbox bash -c "cat > //workspace/path/to/file << 'EOF'\n...\nEOF"` or write content via a heredoc through Docker.
- **Deleting files**: MUST go through the Docker sandbox (already documented under Cleanup below).
- **Executing code** (running scripts, R, Python, shell commands): ALL execution MUST go through the Docker sandbox as described below.

# Common Commands

**Rebuild the Docker image** (host only, after editing Dockerfile):
```
docker compose build
```

**Run a standalone R script:**
```
docker compose run --rm sandbox Rscript //workspace/SamletScript.R
```

**Run a Python script:**
```
docker compose run --rm sandbox python //workspace/helper/script.py
```

# Terminal & Docker Sandbox
- **ALL terminal commands MUST be run inside the Docker sandbox**, not on the host Windows machine.
- Always prefix terminal commands with `docker compose run --rm sandbox`.
- Exception: commands that manage Docker itself (e.g. `docker compose build`) must run on the host.
- Never run `pip install` or any package manager directly on the host — only inside the container or via `docker compose build`.
- **Always run commands yourself** — never ask the user to run terminal commands. Execute them directly using the Bash tool.
- **Auto-run rule**: Always set `SafeToAutoRun: true` for all `docker compose run` commands. These run inside the sandboxed container and are on the user's allow list, so they should never prompt for approval.
- **No special characters in inline commands**: Special characters (`!`, `?`, `&`, `;`, `|`, `()`, `$`, `"`, `'`, backticks) in the command string break the allow-list token matching and cause a manual approval prompt. **Always write code to a helper script file first**, then run the script via the sandbox.
  - Bad: `docker compose run --rm sandbox Rscript -e "rmarkdown::render('/workspace/file.Rmd')"` — quotes and parentheses trigger manual approval
  - Good: Create `helper/_temp_render.R` **via Docker** (e.g. `docker compose run --rm sandbox bash -c "echo ... > //workspace/helper/_temp_render.R"`), then run `docker compose run --rm sandbox Rscript //workspace/helper/_temp_render.R`
  - This applies to ALL commands (R, Python, bash, etc.) — always use the helper script pattern.
- **Cleanup**: If any one-off scratch scripts are created in the `helper/` folder (e.g., `helper/_temp_*.py` or `helper/_temp_*.R`), delete them immediately after use through the Docker sandbox (e.g., `docker compose run --rm sandbox rm //workspace/helper/_temp_render.R`), NOT with host commands like `del` or `Remove-Item`.
- **Git Bash path mangling**: When running Docker commands from Git Bash on Windows, paths starting with `/workspace` get converted to Windows paths (e.g., `C:/Program Files/Git/workspace`). Always use `//workspace` instead of `/workspace` in Docker run commands to prevent this.

# Adding New Packages to Dockerfile (Caching Rules)
To ensure the Docker build process is fast and iterative, you must avoid invalidating the Docker layer cache for early, heavy installations.
1. **DO NOT** add new `apt-get`, `tlmgr`, or `install2.r` commands to the top of the Dockerfile during active development.
2. **DO** append new package installation commands at the very bottom of the Dockerfile (just before the final `USER sandbox` line).
3. If the installation requires root privileges, temporarily switch to root (`USER root`), run the installation, and switch back (`USER sandbox`).
<!-- END: .agents/rules/docker.md -->

<!-- BEGIN: .agents/rules/no_latex.md -->
# Communication
Never use LaTeX code or math formatting (like \mu, \Sigma, $, etc.) when communicating with the user.
<!-- END: .agents/rules/no_latex.md -->

<!-- BEGIN: .agents/rules/project_context.md -->
# Project: Liv2 Compulsory Exercise (Due 2026-03-22)

## What This Is

This is a university-level compulsory exercise for the course "Topics in Life Insurance" (Liv2), Block 3, 2026, taught by Mogens Bladt & Jamaal Ahmad at the University of Copenhagen. Must be approved to participate in the exam. Group work (up to 3), submitted via Absalon.

## Topic

A traditional Danish life-cycle unit-link product design. We examine a 30-year-old in a survival model (alive/dead with mortality rate mu) with:

- **Active phase (age 30 to m=70):** Pension contributions (fraction theta=0.12 of labour income) into a unit-link account, plus a term life insurance (factor K=4 of labour income) payable on death.
- **Retirement phase (age 70+):** Savings pay out a life annuity based on a calculation basis (r_tilde, mu_tilde).
- **Life-cycle investment strategy:** 100% risky assets before age 55, linearly decreasing to 50% at retirement, then 50% after retirement.

## Exercise Structure (7 Parts)

| Part   | Topic |
|--------|-------|
| (i)    | Calculate reserve V_tilde_0 via backward Thiele ODE from max age 111 |
| (ii)   | Simulate single path of account X to age 111 (Euler, h=1/10000) using SDEs (1) and (2) |
| (iii)  | Plot simulation, comment on result, report savings at retirement |
| (iv)   | Argue market reserve equals account value: V^0(t,x) = x |
| (v)    | Show life annuity benefit Y(t) is a generalised GBM, derive dynamics |
| (vi)   | Simulate N=1000 paths of life annuity benefits (Euler, h=1/100) using X(m) from (ii) |
| (vii)  | Plot expected life annuity benefits through time, comment on payout profile |

## Key Parameters

| Parameter | Value |
|-----------|-------|
| r         | 0.02 |
| alpha     | 0.04 |
| sigma     | 0.13 |
| m         | 70 |
| theta     | 0.12 |
| K         | 4 |
| L(t)      | 600000 * exp(0.018*(t-30)) |
| r_tilde(t)| pi(t)*alpha + (1-pi(t))*r |
| mu_tilde(t)| mu(t) |

## Relevant Files

```
AfleveringLiv2/
├── Compulsory exercise.pdf        Official assignment specification
├── mortality.csv                  Mortality rates from Danish FSA (2025 benchmark)
├── SamletScript.R                 Main R script with calculations
├── SimPath.rds                    Saved simulation path data
├── main.tex                       Main LaTeX document (includes all sections)
├── main.pdf                       Compiled PDF output
├── Sections/
│   ├── exercise_i.tex             through exercise_vii.tex (one per exercise part)
├── scripts/
│   └── compile.sh                 LaTeX compilation script
└── AfleveringLiv2.Rproj           RStudio project file
```

## R Environment

Key packages: `tidyverse`, `latex2exp`. Mortality data loaded from `mortality.csv` and interpolated with `approxfun`.
<!-- END: .agents/rules/project_context.md -->
