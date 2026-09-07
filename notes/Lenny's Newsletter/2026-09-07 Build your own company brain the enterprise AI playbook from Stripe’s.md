# Build your own company brain: the enterprise AI playbook from Stripe’s engineering team | Sharadh Krishnamurthy

**Source**: [Lenny's Newsletter](https://www.lennysnewsletter.com/p/build-your-own-company-brain-the)
**Author**: Lenny Rachitsky (featuring Sharadh Krishnamurthy) | **Date**: Sep 07, 2026

---

## Summary

Stripe built Kai, an internal AI agent used by over 10,000 employees weekly, by developing a custom infrastructure that combines governance, skills management, and secure data access rather than relying on off-the-shelf tools. The episode covers the architectural decisions, rollout strategy, and lessons learned from operating AI agents at enterprise scale.

## Key Takeaways

- **Build governance into your AI infrastructure** by using 'projects' as a control mechanism that defines data access, permissions, and audit trails for agents, rather than treating them as simple file folders.
- **Separate skills from tools** to scale AI capabilities—let employees package reusable workflows as skills that agents can compose safely, rather than giving agents direct access to every system.
- **Design your data layer for agent safety** by using tools like Trino to create queryable, auditable access patterns that agents can use without direct database access or risk of taking down production systems.
- **Implement load shedding and agent identity controls** to prevent rogue agents from overwhelming infrastructure, including rate limiting, request validation, and clear identity tracking for every agent action.
- **Plan your rollout with clear skill quality gates** using evals and telemetry from day one, so you can maintain standards as employee-created skills scale to thousands of workflows.

## Related

- [[2026-04-20 How Intercom 2x'd their engineering velocity in 9 months with Claude Code Brian]]
- [[2026-06-17 How to design AI agent loops schedules, goals, and subagents in Claude Code and]]
- [[2026-05-24 The AI paradox More automation, more humans, more work Dan Shipper]]
