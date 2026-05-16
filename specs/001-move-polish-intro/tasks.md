# Task Breakdown: Move Polish Intro Before Chinese Summary

## Phase 1: Analyze and Confirm

1. Review `layouts/single.html` to confirm where the Polish listening block and content are rendered.
2. Identify the target Polish learning markdown entries under `content/posts/` that use the "🇵🇱 波兰语学习 (3分钟速成)" section.
3. Determine whether the content order should be fixed via template logic or by reordering specific Markdown sections.

## Phase 2: Implement Order Adjustment

4. If needed, update `layouts/single.html` so the "三分钟学波兰语" heading and Polish text are rendered before the Chinese summary for the learning content.
5. If the order is controlled in Markdown content, update the relevant `content/posts/*.md` files to place the Polish text block before the Chinese summary.
6. Ensure the Chinese summary remains present and visible after the Polish text.

## Phase 3: Validate

7. Run `hugo server` locally and preview a representative Polish learning page.
8. Verify that the listening section shows Polish text first, then the Chinese summary, and that the audio block still appears.
9. Check for pages with multiple "三分钟学波兰语" modules and confirm consistent ordering.

## Phase 4: Review and Commit

10. Review the changed files and confirm they match the feature spec and implementation plan.
11. Commit the branch with a descriptive message such as `fix: move Polish intro before Chinese summary`.
