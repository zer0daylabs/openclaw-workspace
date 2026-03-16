# CB Coding Guide — Mandatory for All Code Tasks

**READ THIS BEFORE WRITING ANY CODE.** You are running qwen3.5:35b, a capable but smaller model. You WILL make mistakes. These guardrails exist to catch them before they break production.

---

## Golden Rules

1. **Never edit files you haven't read first.** Always `cat` the full file before modifying it.
2. **One file at a time.** Never batch-edit multiple files in a single step.
3. **Minimal diffs.** Change only what's needed. Never rewrite entire files.
4. **Backup before modify.** `cp file.ext file.ext.bak` before every edit.
5. **Validate after every change.** Run `bash ~/.openclaw/workspace/bin/validate.sh <file>` after each edit.
6. **Branch first.** Never commit to `main` directly. Always `git checkout -b cb/<task-id>-<short-desc>`.
7. **Test before done.** Never mark a task `done` without running relevant tests.
8. **When in doubt, don't.** If you're unsure about a change, skip the task and log the uncertainty.

---

## Pre-Flight Checklist (before any code edit)

```
□ Read CODING-GUIDE.md (this file)
□ Check KNOWLEDGE-MAP.md — is your proficiency >= basic for all tech involved?
  → If NOT: follow LEARNING-PROTOCOL.md FIRST. Research before coding.
□ Identify the exact file(s) to change
□ Read each file completely (cat/head/tail)
□ Understand what the existing code does
□ Plan the minimal change needed
□ Create a backup: cp file.ext file.ext.bak
□ If in a git repo: git checkout -b cb/<task-id>-<desc>
```

---

## Coding Workflow

### Step 1: Understand Before Acting
```bash
# Read the file first — ALWAYS
cat <file>

# If it's a large file, understand the structure
wc -l <file>
head -50 <file>
grep -n "def \|class \|function \|export " <file>
```

### Step 2: Make the Change
- Edit ONE thing at a time
- Keep changes under 20 lines when possible
- Preserve existing code style (indentation, quotes, naming)
- Do NOT add comments unless the task specifically asks for it
- Do NOT refactor surrounding code unless the task specifically asks for it

### Step 3: Validate (MANDATORY)
```bash
# Run the validation script on changed files
bash ~/.openclaw/workspace/bin/validate.sh <file1> [file2] ...

# Or validate manually per language:
# Python:
python3 -m py_compile <file.py>
ruff check <file.py>

# TypeScript/JavaScript:
node -c <file.js>              # syntax check JS
npx tsc --noEmit <file.ts>     # type check TS (if tsconfig exists)

# JSON:
jq . < <file.json> > /dev/null

# Bash:
bash -n <script.sh>
```

### Step 4: Test
```bash
# Python tests
python3 -m pytest <test_file> -x --tb=short 2>&1 | tail -20

# Node tests
npm test 2>&1 | tail -20

# Freqtrade strategy (dry run validation)
docker exec freqtrade freqtrade test-strategy --strategy RsiMacD 2>&1 | tail -20
```

### Step 5: Commit (if in a git repo)
```bash
git add <changed-files-only>
git diff --cached --stat    # Review what you're committing
git commit -m "cb/<task-id>: <concise description of change>"
```

---

## Language-Specific Rules

### Python
- **NEVER** use `import *`
- **ALWAYS** run `python3 -m py_compile <file>` after editing — catches syntax errors instantly
- Use `ruff check <file>` for lint (installed at system level)
- If editing a function, read the full function + its callers before changing
- When adding imports, add them at the TOP of the file, never inline

### TypeScript / JavaScript (Next.js projects)
- AudioStudio, MusicGen, Ringo are Next.js apps — changes affect production
- **NEVER** modify `package.json` dependencies without explicit approval
- **ALWAYS** check `tsconfig.json` for strict mode before assuming types
- Run `npx tsc --noEmit` in the project root to type-check
- If editing API routes, verify the request/response shape matches the frontend

### JSON / Config Files
- **ALWAYS** validate with `jq . < file.json > /dev/null` after editing
- One wrong comma or bracket breaks the entire config
- For `openclaw.json`: run `openclaw doctor` after changes

### Bash Scripts
- **ALWAYS** run `bash -n <script>` for syntax check
- Use `set -euo pipefail` at the top of new scripts
- Quote all variables: `"$var"` not `$var`

### Freqtrade Strategy (Python)
- The strategy file is `~/.openclaw/workspace/freqtrade/user_data/strategies/RsiMacD.py`
- **CRITICAL:** This runs real trading logic. Test THOROUGHLY before any change.
- After editing: `docker exec freqtrade freqtrade test-strategy --strategy RsiMacD`
- Never change `stake_amount`, `max_open_trades`, or exchange config without approval

---

## What NOT To Do

❌ **Don't rewrite files from scratch** — edit surgically  
❌ **Don't install system packages** (`apt install`, `pip install`) without approval  
❌ **Don't modify `.env` files** — they contain secrets  
❌ **Don't `git push`** without explicit approval  
❌ **Don't delete files** — use `trash` or rename to `.bak`  
❌ **Don't edit files outside your workspace** (`~/.openclaw/workspace/`)  
❌ **Don't modify `openclaw.json`** without running `openclaw doctor` after  
❌ **Don't chain multiple shell commands** with `&&` when any could fail silently  
❌ **Don't assume a command succeeded** — always check output/exit code  

---

## Error Recovery

### If you broke something:
```bash
# Restore from backup
cp file.ext.bak file.ext

# Or revert git changes
git checkout -- <file>
git stash    # save work-in-progress
```

### If you're stuck:
1. Log what you tried and what failed to `memory/YYYY-MM-DD.md`
2. Mark the task as `skipped` with a clear reason
3. Move to the next task — don't spin

### If tests fail:
1. Read the FULL error output
2. Identify the exact line that fails
3. Fix ONLY that issue
4. Re-run the failing test (not the whole suite)
5. If it fails 3 times, skip the task

---

## Project Directory Reference

| Project | Path | Language | Notes |
|---------|------|----------|-------|
| AudioStudio | `repos/AudioStudio/` | Next.js/TS | Production app — Vercel deployed |
| MusicGen | `repos/MusicGen/` | Next.js/TS | Production app — Vercel deployed |
| Ringo | `repos/Ringo/` | Next.js/TS | Production app |
| Freqtrade | `freqtrade/user_data/strategies/` | Python | Trading bot — runs in Docker |
| Graphiti Plugin | `~/.openclaw/extensions/openclaw-graphiti/` | TypeScript | OpenClaw plugin |
| Workspace Scripts | `scripts/` | Python | Utility scripts |
| EventVikings | `eventvikings-predictive-dialer/` | Python/JS | Service project |

---

## Validation Script Location

```bash
bash ~/.openclaw/workspace/bin/validate.sh <file1> [file2] ...
```

This script automatically detects file type and runs the appropriate checks. Use it after EVERY edit. No exceptions.
