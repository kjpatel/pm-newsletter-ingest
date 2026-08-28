# How to build a Company Operating System with Hermes and OpenClaw

**Source**: [Product Growth](https://www.news.aakashg.com/p/company-os-hermes-openclaw)
**Author**: Aakash Gupta (featuring Mikhail Shcheglov) | **Date**: Aug 28, 2026

---

## Summary

This article provides a practical guide for building a Company Operating System using Hermes and OpenClaw that runs 24/7 on Slack/Telegram with self-improvement capabilities, featuring insights from a CPO who deployed this in production for 5 months.

## Key Takeaways

- **Measure product context coverage first** - Create a knowledge graph dashboard tracking your understanding of industry, business, and customers (aiming for 70-90% coverage before delegating strategy work), using a harsh self-assessment prompt to identify critical knowledge gaps.
- **Build three-layer memory architecture** - Implement raw transcripts (append-only, never summarized), vector embeddings with hybrid retrieval, and knowledge graphs as your foundation, prioritizing recall over summarization since summarizing costs 20-25% accuracy.
- **Define imperatives in a precedence hierarchy** - Create a SOUL.md file establishing rules that prioritize truth over resemblance of good output, with clear layers: truth (no fabrications), personal interests (security/confidentiality), execution (no task deflection), and style.
- **Fork the open-sourced skeleton and supply vital context** - Grab Mikhail's production agent structure from GitHub and use specific prompts to rebuild it into your runtime, configure environment variables, and interview yourself to write USER.md and MEMORY.md files.
- **Let Hermes drive automated skill generation** - Allow the system to watch which tasks you request most frequently and automatically build them as reusable skills, enabling the OS to improve itself without manual intervention.

## Related

- [[2026-03-30 How to Turn Claude Code into Your Personal Life Operating System Hilary Gridley]]
- [[2026-03-24 State of the product job market in early 2026]]
- [[2026-06-17 The AI Product Operating Model]]
