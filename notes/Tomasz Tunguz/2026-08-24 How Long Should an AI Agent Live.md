# How Long Should an AI Agent Live?

**Source**: [Tomasz Tunguz](https://www.tomtunguz.com/how-long-should-an-agent-live/)
**Author**: Tomasz Tunguz | **Date**: Aug 24, 2026

---

## Summary

AI agents should operate on daily 24-hour cycles with ephemeral task specialists rather than perpetual sessions, as long-running sessions suffer from context degradation, security vulnerabilities, and memory poisoning risks.

## Key Takeaways

- **Design agents with 24-hour lifecycles** that reset daily like human workdays, delegating specific tasks to narrow single-purpose specialists that live for only 30 seconds each.
- **Persist state to local files** through a midnight consolidation pass that saves durable learnings and preferences to disk while discarding temporary conversation history.
- **Avoid perpetual sessions** because agent memory degrades over time like human memory, temporary commands become permanent ghosts, and multi-year access credentials create security exposure to malicious injection attacks.
- **Implement stateless task executors** with narrow system prompts that perform single jobs with specific tools, report results, and terminate immediately rather than maintaining conversational context.

## Related

- [[2026-05-26 Agent Gravity Who's Running Your Agents]]
- [[2026-04-10 Founders, Equip Your Agents]]
- [[2026-05-08 Securing the Agentic Enterprise]]
