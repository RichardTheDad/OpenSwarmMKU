# Small Business Marketing Swarm — Customization Guide

This file gives coding agents (Cursor, Claude Code, Codex, etc.) everything they need to understand and customize this swarm. Read it before making any changes.

---

## What is This Swarm?

This is a **Small Business Marketing Swarm** — a multi-agent AI team that creates high-quality marketing materials for local small businesses. It does NOT post automatically. A human reviews everything before it reaches any client or platform.

Built for a web developer who builds websites for local small businesses and provides marketing services to some clients.

---

## Core Philosophy

- **Human review always comes first.** Nothing gets posted automatically.
- **No fake claims.** No invented prices, offers, testimonials, awards, or statistics.
- **Local and specific.** Content must sound like a real local business, not generic AI filler.
- **Client folder is the source of truth.** All content is grounded in `clients/[client-name]/` files.

---

## Folder Structure

```
swarm.py                  ← Main config: imports all agents, defines how they connect
shared_instructions.md    ← Context shared across every agent
run.py                    ← CLI entry point (terminal demo)
server.py                 ← API entry point (FastAPI server)

clients/                  ← One folder per client
  example-client/
    client-brief.md       ← Business overview, target customer, tone, goals
    brand-guide.md        ← Colors, fonts, logo, visual style
    services.md           ← Exact services offered
    offers.md             ← Current confirmed promotions only
    testimonials.md       ← Real approved customer quotes
    approved-language.md  ← Phrases to use
    banned-claims.md      ← What never to say
    assets/               ← Client logos, photos, brand files
    outputs/              ← All generated content (drafts awaiting human review)

orchestrator/             ← Marketing Director
  orchestrator.py
  instructions.md

deep_research/            ← Local Market Research Agent
  deep_research.py
  instructions.md

docs_agent/               ← Content Copywriter
  docs_agent.py
  instructions.md
  tools/

image_generation_agent/   ← Creative Asset Agent
  image_generation_agent.py
  instructions.md
  tools/

video_generation_agent/   ← Short-Form Video Agent
  video_generation_agent.py
  instructions.md
  tools/

data_analyst_agent/       ← Marketing Report Agent
  data_analyst_agent.py
  instructions.md
  tools/

virtual_assistant/        ← Client Ops Agent
  virtual_assistant.py
  instructions.md
  tools/

marketing_qa_agent/       ← Marketing QA Agent (NEW)
  marketing_qa_agent.py
  instructions.md

shared_tools/             ← Tools available to all agents
```

---

## Current Agents

| Agent | Folder | Purpose |
|---|---|---|
| **Marketing Director** | `orchestrator/` | Routes all tasks, assembles content packages, ensures nothing reaches clients without human review |
| **Local Market Research Agent** | `deep_research/` | Researches local competitors, customer search intent, local SEO keywords, seasonal angles |
| **Content Copywriter** | `docs_agent/` | Writes Facebook posts, GBP posts, blog drafts, ad copy, email/newsletter copy, website copy |
| **Creative Asset Agent** | `image_generation_agent/` | Creates graphic concepts, image-gen prompts, promo graphic ideas, ad creative concepts |
| **Short-Form Video Agent** | `video_generation_agent/` | Writes reel scripts, shot lists, voiceover scripts, text overlay plans |
| **Marketing Report Agent** | `data_analyst_agent/` | Builds monthly performance reports from real data — never fakes numbers |
| **Client Ops Agent** | `virtual_assistant/` | Organizes deliverables, content calendars, approval checklists, client packages |
| **Marketing QA Agent** | `marketing_qa_agent/` | Reviews all deliverables before client delivery — checks for fake claims, generic AI language, missing CTAs |

---

## How Agents Connect (`swarm.py`)

`swarm.py` is the only file you need to edit when adding, removing, or rewiring agents. The default pattern is **orchestrator-to-all**: the Marketing Director can send messages to every specialist. All agents can also hand off to each other directly.

---

## Typical Workflows

### Monthly Content Package

1. User tells Marketing Director: "Create a monthly content package for [client]"
2. Marketing Director reads `clients/[client-name]/client-brief.md`
3. Parallel: Local Market Research Agent (research) + Content Copywriter (drafts) + Creative Asset Agent (concepts) + Short-Form Video Agent (reel scripts)
4. Client Ops Agent builds content calendar and approval checklist
5. Marketing QA Agent reviews all content
6. User reviews the final package before anything goes to the client

### One-Off Post

1. User requests a specific post
2. Marketing Director routes to Content Copywriter (Handoff for single-agent task)
3. Content Copywriter reads client files and writes the post
4. Marketing QA Agent reviews
5. User approves before use

### Monthly Report

1. User provides data exports (CSV, screenshots, or connects analytics tools)
2. Marketing Report Agent processes data and builds the report
3. User reviews and delivers to client

---

## Key Conventions

- Each agent folder has one `<name>.py` and one `instructions.md`
- `instructions.md` is the agent's system prompt — edit it to change behavior
- Tools live in `tools/` and are auto-loaded by the agent definition
- `shared_tools/` contains Composio-powered integrations available to all agents
- Models are configured via `DEFAULT_MODEL` in `.env` — never hardcoded

---

## How to Add a New Client

1. Copy `clients/example-client/` to `clients/[new-client-name]/`
2. Fill in all the template files
3. Tell the swarm: "Create a content package for [client name] — brief is at clients/[client-name]/"

---

## How to Customize Further

To adapt this swarm for a different use case:

1. Update `instructions.md` for the relevant agent(s)
2. Update `shared_instructions.md` if the swarm-wide rules change
3. Update `swarm.py` if you add or remove agents
4. Update this file to reflect any structural changes
