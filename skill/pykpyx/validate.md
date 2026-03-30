# /pykpyx validate

You are executing the `validate` sub-command. This validates a game spec against the engine's rules and produces a validation report.

## Arguments

- `[path/to/spec.md]` (optional) — path to the spec file to validate.

If no path is provided:
1. Look for `.md` files in `specs/` (excluding files ending in `-VALIDATION.md`).
2. If exactly one is found, use it.
3. If multiple are found, list them and ask the human which one to validate.
4. If none are found, tell the human to create a spec first with `/pykpyx create`.

## Workflow

### 1. Load validation rules

Read the validation checklist from `<skill-dir>/docs/VALIDATION-CHECKLIST.md`. This file defines every rule to check, grouped by section.

### 2. Read the spec

Read the spec file at the given path. If the file does not exist, stop and report the error.

### 3. Resolve supplementary specs

Check the spec content for `@specs/` references or markdown hyperlinks to other `.md` files. If found, read those files too — they provide additional detail for validation (e.g. enemy definitions, HUD layout). The primary spec is still the main file being validated.

### 4. Apply validation rules

Work through each rule group in the checklist. For each rule:

- Determine **PASS** or **FAIL** based on the spec content.
- For **FAIL**: note the specific issue and write a concrete suggested fix (e.g. *"Add a `Game Type` section with value `Game` or `RPGGame`"*).
- Skip rule groups that don't apply (e.g. skip "RPG-specific Rules" if Game Type is `Game`).

### 5. Generate summary (if all rules pass)

If every rule passes, produce a generation preview:

- **Game type** and derived directory name
- **Files that will be generated** (main.py, game_loop.py, game_load.py, and sprites.py if ≥ 4 sprites)
- **Sprite count** (total number of sprites defined)
- **Signal count** (number of signals that will be wired based on Input, Game Type, and HUD)
- **GameState fields** (list of field names and types)

### 6. Write validation report

Write the report to `specs/<SPEC-NAME>-VALIDATION.md`, where `<SPEC-NAME>` is the spec filename without the `.md` extension.

**Report format:**

```markdown
# Validation Report: <Spec Filename>

**Date:** <today's date>
**Status:** PASS | FAIL (<n> issues)

---

## Structure Rules

- [x] "Game Type" section exists
- [ ] "Sprites" section exists — **FAIL:** No sprites defined. Add at least one sprite under the Sprites section.

## Game Type Rules

- [x] Game Type value is `Game` or `RPGGame`
...

---

## Summary

<If all pass: generation preview as described above>
<If any fail: count of issues and recommendation to fix and re-validate>
```

If a report file already exists at that path, **overwrite it** — validation reports are regenerated each time.

### 7. Report to the human

- If all rules pass: *"Spec is valid. Run `/pykpyx generate specs/<SPEC-NAME>.md` to generate your game."*
- If any rules fail: *"N issues found in specs/<SPEC-NAME>.md. See `specs/<SPEC-NAME>-VALIDATION.md` for details."*

Always mention the path to the validation report file.
