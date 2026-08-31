# How Long Should an AI Agent Live?

**Source**: [Tomasz Tunguz](https://tomtunguz.com/how-long-should-an-agent-live/)
**Author**: Tomasz Tunguz | **Date**: Aug 24, 2026

---

## Summary

AI agents should operate on 24-hour reset cycles with delegated ephemeral specialists rather than perpetual sessions, as long-running sessions suffer from context degradation, security vulnerabilities, and permanent behavioral drift.

## Key Takeaways

- **Design daily coordinators** that reset every 24 hours and persist only essential preferences to local files, preventing context rot and security exposure from accumulated session data.
- **Delegate to ephemeral specialists** that live for seconds with narrow, single-purpose tools (calendar agents, email agents, news agents) rather than giving one agent permanent multi-year access.
- **Implement offline consolidation** that summarizes each day's learnings into persistent rules files at midnight, preserving important preferences while discarding conversational chatter that causes agent drift.
- **Avoid perpetual sessions** which accumulate false memories (like cancelled meetings from months prior), degrade attention across growing context, and create security vulnerabilities for poisoning attacks.

## Related

- [[2026-08-07 The Secret Chat Room]]
- [[2026-05-26 Agent Gravity Who's Running Your Agents]]
- [[2026-05-08 Securing the Agentic Enterprise]]
