# PM's Guide to Karpathy's Autoresearch

**Source**: [Product Growth](https://www.news.aakashg.com/p/autoresearch-guide-for-pms)
**Author**: Aakash Gupta | **Date**: Mar 20, 2026

---

## Summary

Autoresearch is a pattern for autonomously iterating on and optimizing any measurable system (prompts, skills, code) by running hundreds of experimental rounds overnight, and PMs can apply this beyond ML by defining clear metrics and using coding agents to automate the optimization loop.

## Key Takeaways

- **Define a clear numeric metric** for what you want to optimize—replace subjective judgments like 'Is this good?' with measurable yes/no criteria that can be scored programmatically across test runs.
- **Build an evaluation script that runs autonomously** using Claude Code or similar agents so the feedback loop runs without human intervention, enabling dozens of experiments to complete overnight.
- **Isolate the single file the agent can modify** (your prompt, skill, or system instruction) while keeping everything else read-only, preventing the agent from gaming the metric instead of genuinely improving performance.
- **Apply autoresearch to any skill stuck at 70-80% accuracy** by setting up the three-part structure: measurable metric + autonomous eval tool + single editable file, which unlocks 50+ iterations you'd never manually complete.
- **Use the experiment log as your primary artifact**, not just the final result—the log shows you what changes the agent discovered, which often reveals bugs or insights in your original implementation.

## Related

- [[A Guide to Claude Code for PMs From Cowork to Code]]
- [[How to Build Product Strategy in the Age of AI Step-by-Step with Claude Code]]
- [[Agents Over Bubbles]]
