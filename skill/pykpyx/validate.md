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

### Important: Interpreting `colrow()` notation

The spec uses `colrow(<col>,<row>)` notation (e.g. `colrow(3,5)`) to make it unambiguous that the first value is a **column** and the second is a **row**. When validating coordinates:

- Strip the `colrow(` prefix and `)` suffix to extract the two integer values.
- The first value is the column, the second is the row — both must be positive integers (1-indexed).
- Also accept bare `(<col>,<row>)` as valid (backwards compatibility), but flag a **WARNING** suggesting the human use `colrow()` for clarity.

### Important: Interpreting empty values

The human may express "no action" or "not applicable" in several equivalent ways. Treat all of the following as meaning **no value / not applicable**:

- `none`
- `n/a`
- Empty value (key present but blank, e.g. `- **Released:**`)
- Absent key (sub-item omitted entirely)

Never flag these as missing or incomplete. They all mean the same thing: this field intentionally has no value.

### 4. Apply validation rules

Work through each rule group in the checklist. For each rule:

- Determine **PASS** or **FAIL** based on the spec content.
- For **FAIL**: note the specific issue and write a concrete suggested fix (e.g. *"Add a `Game Type` section with value `Game` or `RPGGame`"*).
- Skip rule groups that don't apply (e.g. skip "RPG-specific Rules" if Game Type is `Game`).

### 5. Scan for redundancy

Apply the **Consistency and Redundancy Rules** from the checklist. For each redundancy found:

- Identify the sections that contain the duplicated or conflicting information.
- Recommend which section should own that information and what should be removed from the other sections.
- Mark as **FAIL** — the human must consolidate the redundancy and re-run validate.

Common redundancies to watch for:
- Movement speed stated in both Entities and Sprites (or Input, or Game Update)
- Entity behaviour described in both Entities and Game Update with conflicting detail
- Input actions using sprite names instead of entity names

### 6. Flag natural-language ambiguity

Scan the **Game Start**, **Game Update**, and **Entity descriptions** for natural-language content that could be interpreted multiple ways. For each ambiguity found:

- Mark as **WARNING** (not FAIL) in the report.
- Describe what is ambiguous and suggest how the human could clarify it.
- Note that the `generate` command will prompt for clarification at generation time if these are not resolved.

Examples of ambiguity to flag:
- Positions described in relative terms without coordinates (e.g. "centre of the screen", "near the top")
- Vague timing or conditions (e.g. "after a while", "sometimes")
- References to concepts not defined elsewhere in the spec

### 7. Generate summary (if all rules pass and no redundancies found)

If every rule passes and no redundancies are found, produce a generation preview. Warnings (ambiguity) do not block the summary.

- **Game type** and derived directory name
- **Files that will be generated** (main.py, game_loop.py, game_load.py, and sprites.py if ≥ 4 sprites)
- **Sprite count** (total number of sprites defined)
- **Signal count** (number of signals that will be wired based on Input, Game Type, and HUD)
- **GameState fields** (list of field names and types)

### 8. Write validation report

Write the report to `specs/<SPEC-NAME>-VALIDATION.md`, where `<SPEC-NAME>` is the spec filename without the `.md` extension.

**Report format:**

```markdown
# Validation Report: <Spec Filename>

**Date:** <today's date>
**Status:** PASS | FAIL (<n> issues) | PASS WITH WARNINGS (<n> warnings)

---

## Structure Rules

- [x] "Game Type" section exists
- [ ] "Sprites" section exists — **FAIL:** No sprites defined. Add at least one sprite under the Sprites section.

## Game Type Rules

- [x] Game Type value is `Game` or `RPGGame`
...

## Consistency and Redundancy

- [ ] Movement speed defined only in Entities — **FAIL:** Speed "10 px per second" appears in both Entities > Player and Sprites > Ship. Remove speed from the Sprites section.
...

## Ambiguity Warnings

- ⚠️ Game Start: "centre of the screen" — consider specifying exact `colrow(<col>,<row>)` coordinates, or the generate command will prompt for clarification.
...

---

## Summary

<If all pass (no FAIL): generation preview as described above>
<If any FAIL: count of issues and recommendation to fix and re-validate>
<If PASS with warnings: generation preview + note that generate will prompt for clarification on warnings>
```

If a report file already exists at that path, **overwrite it** — validation reports are regenerated each time.

### 9. Report to the human

- If all rules pass (no warnings): *"Spec is valid. Run `/pykpyx generate specs/<SPEC-NAME>.md` to generate your game."*
- If all rules pass with warnings: *"Spec is valid with N warnings. Run `/pykpyx generate specs/<SPEC-NAME>.md` to generate — you'll be prompted to clarify ambiguous sections. See `specs/<SPEC-NAME>-VALIDATION.md` for details."*
- If any rules fail: *"N issues found in specs/<SPEC-NAME>.md. See `specs/<SPEC-NAME>-VALIDATION.md` for details."*

Always mention the path to the validation report file.
