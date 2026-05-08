<div align="center">

# Small Business Marketing Swarm

![OpenSwarm](assets/new-framework.jpg)

</div>

**A human-reviewed multi-agent marketing system for local small businesses.**

Creates monthly content packages, social media posts, ad creatives, SEO content, Google Business Profile updates, video scripts, and monthly reports — all drafted for human review before anything reaches a client or gets posted.

Built on [Agency Swarm](https://github.com/VRSEN/agency-swarm).

---

## How It Works

8 specialist agents collaborate to create marketing deliverables. A human reviews everything. Nothing is posted automatically.

```
You → Marketing Director → Specialists → QA Review → You review → Client
```

**Key rules baked into every agent:**
- No automatic posting or publishing
- No invented prices, offers, testimonials, events, or guarantees
- Content must be specific to the local business — no generic AI filler
- Every post must have a clear purpose and CTA
- Everything is a draft until you approve it

---

## The Team

| Agent | What it does |
|---|---|
| **Marketing Director** | Entry point. Routes client requests to the right specialists. Assembles the final package. |
| **Local Market Research Agent** | Researches local competitors, customer search intent, local SEO keywords, and seasonal content angles. Always cites sources. |
| **Content Copywriter** | Writes Facebook posts, Google Business Profile posts, blog drafts, ad copy, email/newsletter copy, and website marketing copy. Avoids generic AI language. |
| **Creative Asset Agent** | Creates graphic concepts, image-generation prompts, promo graphic ideas, and ad creative concepts. Generates actual AI images when needed. |
| **Short-Form Video Agent** | Writes reel scripts, shot lists, voiceover scripts, and text overlay plans. Designed for phone-filmable content. |
| **Marketing Report Agent** | Turns real website/social/GBP data into readable monthly reports. Never invents or estimates numbers. |
| **Client Ops Agent** | Organizes deliverables, content calendars, approval checklists, and client packages. Does not post anything without explicit instruction. |
| **Marketing QA Agent** | Reviews all deliverables before you see them — checks for fake claims, generic AI language, missing CTAs, and brand inconsistencies. |

---

## Client Folder Structure

Each client gets their own folder:

```
clients/
  your-client-name/
    client-brief.md       ← Business overview, target customer, tone, goals
    brand-guide.md        ← Colors, fonts, logo, visual style
    services.md           ← Exact services offered (only these get written about)
    offers.md             ← Current confirmed promotions (empty = no offers)
    testimonials.md       ← Real approved customer quotes
    approved-language.md  ← Phrases to use
    banned-claims.md      ← What never to say or imply
    assets/               ← Client logos, photos, brand files
    outputs/              ← All generated content (your review queue)
```

**To add a new client:** copy `clients/example-client/`, rename it, and fill in the files.

---

## Getting Started

### 1. Install Dependencies

```bash
git clone https://github.com/VRSEN/openswarm.git
cd openswarm
pip install -r requirements.txt
```

Or use the npm installer:

```bash
npm install -g @vrsen/openswarm
openswarm
```

### 2. Add API Keys

Copy `.env.example` to `.env` and add your keys:

```
OPENAI_API_KEY=...          # Required (or use ANTHROPIC_API_KEY for Claude)
ANTHROPIC_API_KEY=...       # For Claude models
SEARCH_API_KEY=...          # For web research
GOOGLE_API_KEY=...          # For AI image and video generation
FAL_KEY=...                 # For additional video generation
COMPOSIO_API_KEY=...        # For Google Analytics, Drive, Sheets integrations
```

### 3. Set Up a Client

1. Copy `clients/example-client/` to `clients/[your-client-name]/`
2. Fill in `client-brief.md`, `services.md`, and `brand-guide.md` at minimum
3. Add any current offers to `offers.md` (leave empty if none)
4. Add approved testimonials to `testimonials.md`
5. Fill in `banned-claims.md` with anything that must never be said

### 4. Run the Swarm

```bash
python swarm.py
```

Or via API server:

```bash
python server.py   # Runs on localhost:8080
```

---

## Example Requests

Paste these into the terminal when the swarm is running:

**Monthly content package:**
> "Create a full monthly content package for [client name]. Their brief is at clients/[client-name]/. I need 8 Facebook posts, 4 GBP updates, 1 blog draft, and 2 reel scripts for June."

**One-off post:**
> "Write a Facebook post for [client name] about their summer special. Client files are at clients/[client-name]/."

**Local market research:**
> "Research local competitors for [client name], a [business type] in [city]. Save the research brief to their client folder."

**Monthly report:**
> "Here's [client name]'s Google Analytics export and GBP data for May. Create their monthly marketing report."

**Ad campaign:**
> "Create Facebook ad copy and a graphic concept for [client name]'s [service] campaign. Budget is $[X]/day."

---

## Workflow: Monthly Content Package

1. Fill in the client folder (15-20 minutes the first time, 5 minutes to update monthly)
2. Ask the Marketing Director to create the monthly package
3. Specialists run in parallel — research, copy, visuals, video scripts
4. Client Ops Agent organizes everything into a dated delivery folder
5. Marketing QA Agent reviews all content
6. You review the final package in `clients/[client-name]/outputs/`
7. Edit anything you want, then deliver to the client

**Total review time:** typically 20-30 minutes per client per month

---

## API Keys Reference

**Required (choose one):**
- `OPENAI_API_KEY` — for GPT models and OpenAI web search
- `ANTHROPIC_API_KEY` — for Claude models

**Web search (built-in with OpenAI):**
- Web search for the Local Market Research Agent uses the **OpenAI Responses API** (`web_search` tool)
- Only `OPENAI_API_KEY` is needed — no separate search key required
- Configured in `deep_research/tools/OpenAIWebSearchTool.py`

**Optional — academic search only:**
- `SEARCH_API_KEY` (SearchAPI.io) — only needed if you want `ScholarSearch` for academic papers. Not used in normal marketing workflows.

**For visual assets:**
- `GOOGLE_API_KEY` — Gemini image generation
- `FAL_KEY` — Seedance video generation

**For integrations:**
- `COMPOSIO_API_KEY` — Google Analytics, Google Drive, Google Sheets, Meta integrations

All tools degrade gracefully when keys are missing.

---

## Graphic Generation

The Creative Asset Agent supports three output modes depending on what you ask for and which API keys are available.

### Mode 1: Graphic Concepts (default)

No API key needed. The agent writes a detailed description of what each graphic should look like — layout, colors, text, CTA — ready to hand to a designer or build in Canva.

Saved to: `clients/[client-name]/outputs/[month_year]/graphic-concepts/`

### Mode 2: Image-Generation Prompts

No API key needed. The agent writes detailed prompts formatted for Midjourney, DALL-E, or Canva AI — ready to paste directly into any image generation tool.

Saved to: `clients/[client-name]/outputs/[month_year]/image-prompts/`

### Mode 3: Actual Generated Image Files

**Requires `GOOGLE_API_KEY`** (Gemini) or **`OPENAI_API_KEY`** (OpenAI gpt-image-1.5).

The agent generates real PNG files and saves them directly into the client output folder. Generated images must be reviewed by a human before client delivery — they are never sent automatically.

Saved to: `clients/[client-name]/outputs/[month_year]/graphics/`

**Models available:**
| Model | Key Required | Best For |
|---|---|---|
| `gemini-2.5-flash-image` | `GOOGLE_API_KEY` | Social media posts, quick concepts |
| `gemini-3-pro-image-preview` | `GOOGLE_API_KEY` | Ad creatives, hero images |
| `gpt-image-1.5` | `OPENAI_API_KEY` | High-quality output (1:1, 2:3, 3:2 only) |

### How to Request Actual Graphics

In your swarm prompt, explicitly ask for generated image files:

```
Create a full monthly content package for Oxford Golf Academy — client files at clients/oxford-golf-academy/.
I need 8 Facebook posts, 4 GBP updates, and generate actual image files for the top 3 Facebook posts.
Save generated graphics to clients/oxford-golf-academy/outputs/may_2026/graphics/.
```

Without the explicit request, the agent produces concepts only (no images generated, no API cost).

### Logo Workflow — AI Never Draws the Logo

Client logos are NEVER passed to or recreated by any AI image model. AI models redraw logos incorrectly — wrong colors, wrong text, wrong shape.

**Correct workflow (enforced in agent instructions):**

1. `GenerateImages` creates the background only — prompt says "leave upper-left corner clear for logo"
2. `OverlayLogo` composites the real logo file onto the background using Pillow — no AI involved
3. Two files are saved: `[name]_final.png` (with logo) and `[name]_final_raw_bg.png` (background only)

**Logo file location:** `clients/[client-name]/assets/logo.png`

If no `logo.png` exists, the agent generates the background and writes "Logo overlay pending — add official logo to assets/" in the markdown output. It does NOT attempt to draw the logo.

**The Marketing QA Agent checks every graphic** for AI-redrawn logos and flags them automatically.

### Notes

- AI-generated text inside images is often broken — always check before use
- Generated images are drafts — a human must review before sending to any client
- The existing markdown content package is never replaced — graphics are separate additional files

---

## For Developers

**Local development:**

```bash
git clone https://github.com/VRSEN/openswarm.git
cd openswarm
python swarm.py
```

**Docker:**

```bash
cp .env.example .env
docker-compose up --build
```

See [AGENTS.md](AGENTS.md) for the full customization guide.

---

## Built On

- [Agency Swarm](https://github.com/VRSEN/agency-swarm) — multi-agent framework
- [Composio](https://composio.dev) — external integrations

## License

MIT — see [LICENSE](LICENSE).
