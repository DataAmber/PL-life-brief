# Feature Specification: Move Polish Intro Before Chinese Summary

**Feature Branch**: `001-move-polish-intro`

**Created**: 2026-05-16

**Status**: Draft

**Input**: User description: "定义一个spec，我要把三分钟学波兰语放到中文摘要前面， 这样可以听力下面直接是波兰语文本"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Polish learning flow ordering (Priority: P1)

A learner views the Polish learning module and should see the "三分钟学波兰语" heading before the Chinese summary, so the listening section can show the Polish text directly.

**Why this priority**: This change improves comprehension by placing the original Polish content ahead of its translation, which is essential for language learners using the listening exercise.

**Independent Test**: Verify the targeted learning page displays the heading and Polish text in the new order without changing the Chinese summary content.

**Acceptance Scenarios**:

1. **Given** a learner opens the Polish learning page, **When** the page loads, **Then** the "三分钟学波兰语" section title appears before the Chinese summary.
2. **Given** the listening section is visible, **When** the user scrolls to it, **Then** the Polish text appears directly under the listening heading and before the Chinese translation.

---

### User Story 2 - Content clarity for listening practice (Priority: P2)

A learner using the listening section should see the Polish text immediately, rather than seeing the Chinese summary first, to preserve the intended listening practice order.

**Why this priority**: Ensuring the Polish text appears first in the listening section prevents premature translation and keeps the listening exercise aligned with the original language.

**Independent Test**: Confirm the listening exercise block contains the Polish text first and the Chinese summary afterward on the same page.

**Acceptance Scenarios**:

1. **Given** the listening exercise is present, **When** the page is inspected, **Then** the Polish text block is positioned above the Chinese summary within the listening area.

---

### Edge Cases

- What happens if the learning page has multiple "三分钟学波兰语" modules on the same page?
- How does the page handle missing Polish text or missing Chinese summary content?
- What happens if the listening section is absent for this content?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST display the "三分钟学波兰语" heading before the Chinese summary for the targeted Polish learning content.
- **FR-002**: The listening section MUST present the Polish text directly under its heading, before any Chinese translation appears.
- **FR-003**: The Chinese summary MUST remain available and appear after the Polish text in the content order.
- **FR-004**: The updated ordering MUST apply consistently for all relevant "三分钟学波兰语" learning entries.
- **FR-005**: The page layout MUST not remove or hide the Chinese summary when reordering the content blocks.

### Key Entities *(include if feature involves data)*

- **Polish learning module**: A content block or page section containing the title, Polish text, Chinese summary, and listening prompt.
- **Listening section**: The part of the module where audio-related text is shown, including the Polish source text and subsequent translation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The "三分钟学波兰语" heading is visible before the Chinese summary on the target page in 100% of verified cases.
- **SC-002**: The listening section shows Polish text immediately below its heading in 100% of verified cases.
- **SC-003**: The Chinese summary remains present after the Polish text in the same content flow for all reviewed examples.
- **SC-004**: No learner report exists of the Polish listening section starting with the Chinese summary after rollout.

## Assumptions

- This feature applies to the specific Polish learning module and related listening content on the site.
- The page structure supports reordering text blocks without requiring additional translation logic.
- Existing content templates already include separate Polish text and Chinese summary sections.
- The requested change is primarily a presentation/order adjustment rather than a new content creation task.
