# Evals are the new PRD. Here is the playbook with the CEO of the leader in the space (Ankur Goyal, Founder and CEO, Braintrust)

**Source**: [Product Growth](https://www.news.aakashg.com/p/ankur-goyal-podcast)
**Author**: Aakash Gupta (featuring Ankur Goyal) | **Date**: Mar 20, 2026

---

## Summary

Evals have become the new PRD for AI products, replacing subjective vibe checks with structured, scalable measurement frameworks that encode product requirements as data, tasks, and scoring functions. This episode features Ankur Goyal, CEO of Braintrust, building an eval from scratch to demonstrate the complete practitioner's playbook for PMs.

## Key Takeaways

- **Replace vibe checks with structured evals** when your product scales beyond one person's intuition—use the data-task-scores framework to encode what users actually need into testable components that survive model changes.
- **Treat evals as your product specification** rather than an engineering afterthought; encode product intuition as datasets, use scoring functions as success criteria, and iterate on whichever component (data, task, or scores) is the bottleneck.
- **Start with auto-generated synthetic data immediately** rather than spending weeks on perfect golden datasets—jump in with silly test questions, manually edit them, and run your first eval within minutes to begin iterating.
- **Override model post-training behavior explicitly** in your system prompts when building evals; models are trained to ask clarifying questions conversationally, so you must instruct them to use tools and solve problems directly.
- **Use categorical scoring with clear criteria** (A/B/C or Pass/Fail) normalized to 0-1 scales instead of freeform numbers; this forces comparability across model versions and makes it obvious when the eval itself is miscalibrated rather than the product failing.

## Related

- [[2026-02-19 AI Evals Explained Simply by Ankit Shukla]]
- [[2026-03-09 How to Build Product Strategy in the Age of AI Step-by-Step with Claude Code]]
- [[2026-02-13 How to Do AI-Powered Discovery (Step-by-Step with Live Demo) Caitlin Sullivan]]
