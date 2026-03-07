# Is AI Doing Less & Less?

**Source**: [Tomasz Tunguz](https://www.tomtunguz.com/hybrid-state-machine-agents/)
**Author**: Tomasz Tunguz | **Date**: Feb 26, 2026

---

## Summary

The author discovered that the most effective AI systems aren't purely agentic—65% of their agent's workflow nodes now run as deterministic code rather than LLM calls, following Stripe's 'minion architecture' principle that code handles predictable tasks while LLMs tackle ambiguous ones.

## Key Takeaways

- **Use blueprints over prompts** to explicitly control when LLMs are involved in workflows, treating them as decision-making components rather than task executors for the entire pipeline.
- **Segment workflows by predictability** - reserve LLM calls for research, synthesis, and genuinely ambiguous tasks (36% of workflows) while letting deterministic code handle routing and updates (29% of workflows).
- **Implement Stripe's minion architecture** by creating directed graph workflows with both deterministic and agentic nodes, ensuring the LLM only processes constrained inputs it actually needs.
- **Monitor your AI overhead** - track what percentage of your system runs without LLM involvement; the author achieved 67-91% code execution for many workflow types, reducing costs and latency.
- **Plan for capability expansion** - recognize that today's deterministic code solutions may become LLM tasks with future model releases, so build your system architecture with flexibility.

## Related

- [[Not Prompts, Blueprints]]
- [[The PM's Guide to Agent Distribution MCP Servers, CLIs, and AGENTS.md]]
- [[RIP OpenClaw How I Built a Secure Autonomous AI Agent with Claude and n8n]]
