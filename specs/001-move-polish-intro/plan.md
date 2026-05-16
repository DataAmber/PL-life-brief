# Implementation Plan: Move Polish Intro Before Chinese Summary

**Branch**: `001-move-polish-intro` | **Date**: 2026-05-16 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-move-polish-intro/spec.md`

## Summary

Update the Polish learning presentation order so that the “三分钟学波兰语” heading and Polish text appear before the Chinese summary on the target learning page. This is a content/layout adjustment for the Hugo static site, ensuring the listening block surfaces original Polish text first while preserving the Chinese translation afterward.

## Technical Context

**Language/Version**: Hugo static site generator using Go templates and Markdown content.

**Primary Dependencies**: Hugo, project theme, Markdown content files.

**Storage**: Static Markdown files under `content/posts/`; template files under `layouts/`.

**Testing**: Manual preview with `hugo server`; verify content ordering in generated HTML. Optionally use browser DOM inspection or search within the rendered page output.

**Target Platform**: Static website built by Hugo, served as HTML/CSS.

**Project Type**: Web content site / static site.

**Performance Goals**: N/A for this content-order change, but maintain page render correctness.

**Constraints**: Must not remove or hide existing Chinese summary text; ordering change should apply only to relevant Polish learning entries without affecting unrelated article structure.

**Scale/Scope**: This change targets the Polish learning content flow in one or more `content/posts/*.md` entries and the single article layout.

## Constitution Check

*GATE: Confirm that the requested change is scoped to a layout/order adjustment and does not require backend changes or new data models.*

- [x] The feature is a presentation/order change, not a new service.
- [x] Existing Hugo template and content structure are sufficient.
- [x] No new data storage model is required.
- [x] The change can be validated via site preview.

## Project Structure

### Documentation (this feature)

```text
specs/001-move-polish-intro/
├── plan.md
├── spec.md
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
content/
├── posts/
│   ├── ... Polish learning markdown entries
│   └── ...
layouts/
└── single.html
static/
└── audio/
```

**Structure Decision**: Use the existing Hugo static site layout. The fix is implemented by adjusting the rendering of the Polish listening content block in `layouts/single.html` and/or by reordering specific markdown sections in `content/posts/*.md`.

## Complexity Tracking

> No constitution violations detected; this is a small scoped content presentation fix.
