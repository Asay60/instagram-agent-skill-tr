# Instagram Agent TR — Codex and Claude

[Türkçe](README.md) · [Attribution](UPSTREAM.md)

An MIT-licensed adaptation of [Jake Schincariol's instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill), maintained by ASAYTECH / Asay60. Thirteen bilingual workflows and seven local Python tools. Original copyright and license retained.

## Install

Requires Git and Python 3.10+. Local tools need no third-party packages or API key; your agent/model has its own account requirements.

```bash
git clone https://github.com/Asay60/instagram-agent-skill-tr.git
cd instagram-agent-skill-tr
python3 scripts/install.py --agent codex
# or
python3 scripts/install.py --agent claude
```

On Windows use `py -3 -X utf8`. For project scope add `--scope project` from the intended working directory, or provide `--dest`. Existing folders are not replaced without `--overwrite`; backups sit outside skill discovery. Install the whole pack, including `_instagram_agent_shared`.

Use `$ig-reel` in Codex, `/ig-reel` in Claude. See [official Codex documentation](https://developers.openai.com/codex/skills). Codex installation uses local skills, not a bundled marketplace manifest. Claude marketplace metadata is included but has not been tested in a live client.

Copy `templates/voice.en.md` to `~/.instagram-agent/voice.md`, or set `IG_AGENT_HOME` to a separate brand directory. Agent workflows resolve that directory; standalone tools require explicit output paths. Do not commit personal/customer data.

## Workflows

Reel scripts, research using supplied/authorized samples, captions, carousels, Stories, profile audits, weekly plans, editorial cleanup, comments, replies, DMs, repurposing, and performance analysis.

Skills route to Turkish or English references. Shared runtime instructions take precedence over historical platform assertions in English upstream references.

## Tools

```bash
python3 skills/ig-reel/hookscore.py --hook "Your three missed follow-ups cost $500." --lang en --json
python3 skills/ig-reel/beats.py script.txt --lang tr --target 30 --json
python3 skills/ig-caption/caption.py caption.txt --lang tr --json
python3 skills/ig-human/humanize.py draft.txt --lang tr -o clean.txt --report
python3 skills/ig-human/detect.py draft.txt clean.txt --lang tr --json
python3 skills/ig-viral/swipe.py captured.tsv --lang tr --out swipe.md --json
```

Default language is `en`. `--lang tr` changes analysis vocabulary, formulas and relevant heuristics. JSON keys and some technical diagnostics remain English. Hook, caption and style tools may return 1 for editorial warnings while still producing valid analysis.

## Limits

- Draft production only. No Instagram authentication, publishing, comments, DMs, scheduling, scraping or video rendering is included.
- Turkish scores have not been validated on a Turkish Reels corpus. Tests establish software behavior, not marketing performance.
- Hook scores do not predict virality. Style scores do not establish human/AI authorship. Unicode formatting is not evidence of a watermark or AI origin.
- Timings are word-count estimates; verify against recordings.
- Feed preview and hashtag budget are configurable editorial defaults, not verified live platform limits (`--truncate`, `--hashtag-limit`).
- Supply full integer counts to `swipe.py`; K/M/bin abbreviations are rejected. Account medians and follower counts have different denominators; inspect each row's `baseline_kind`.
- Tools run locally without uploads. Sending drafts to an AI agent is subject to your provider's handling.
- Local tests do not verify live Codex/Claude or Instagram end-to-end operation.

## Tests and license

```bash
python3 -m unittest discover -s tests -v
```

See [UPSTREAM.md](UPSTREAM.md), [CHANGELOG.md](CHANGELOG.md), and [LICENSE](LICENSE). Not affiliated with OpenAI, Anthropic or Meta.
