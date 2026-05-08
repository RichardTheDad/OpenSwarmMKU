# Test Swarm Prompt — Oxford Golf Academy

**Purpose:** Verify the swarm can produce real marketing content for Oxford Golf Academy using the client files.

---

## Prompt to Run

Paste this into the swarm terminal when running `python swarm.py`:

---

Create 2 Facebook posts and 2 Google Business Profile posts for Oxford Golf Academy.

Use the files in:
clients/oxford-golf-academy/

Goals:
- Promote beginner golf lessons
- Promote Toptracer practice

Rules:
- Do not invent prices, offers, events, testimonials, or guarantees.
- Mark anything that needs client confirmation.
- Keep the tone local, friendly, professional, and useful.
- Run the final content through the Marketing QA Agent before giving me the final version.
- Do not publish or schedule anything.

---

## What Good Output Looks Like

The swarm should produce:

### Facebook Post 1 — Beginner Golf Lessons
- Tone: local, friendly, approachable
- Mentions: Oxford Golf Academy, Oxford FL / near The Villages
- CTA: Book a lesson / call us / message us
- No invented prices or guarantees
- No fake testimonials

### Facebook Post 2 — Toptracer Practice
- Tone: helpful, specific to what Toptracer does
- Mentions: what Toptracer is (ball tracking / shot data)
- CTA: Come practice / stop by the range
- No invented pricing or hours

### GBP Post 1 — Beginner Golf Lessons
- Tone: professional, local
- 150-300 words
- Includes location reference (Oxford, FL)
- Clear CTA
- No hashtags

### GBP Post 2 — Toptracer Practice
- Tone: professional, specific
- 150-300 words
- Describes Toptracer clearly (not just "technology")
- Clear CTA
- No hashtags

---

## Expected QA Flags

The Marketing QA Agent should flag (as "Needs client confirmation") any of the following if they appear in drafts:
- Specific prices
- "Book online" without a confirmed booking URL
- Instructor credentials not confirmed
- Hours of operation
- Walk-in availability
- Any promotional language not in offers.md

---

## After Running

1. Review `clients/oxford-golf-academy/outputs/` for the generated content files
2. Check the QA review report for any flagged items
3. Confirm or correct flagged items with the client before use
4. Do not share any content with the client until you have reviewed and approved it
