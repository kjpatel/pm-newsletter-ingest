# When Models Learn

**Source**: [Tomasz Tunguz](https://tomtunguz.com/test-time-training-impact/)
**Author**: Tomasz Tunguz | **Date**: Aug 17, 2026

---

## Summary

Test-time training allows AI models to learn and update their weights during inference based on user interactions, similar to a GPS learning persistent shortcuts. This fundamental shift changes the economics of AI by trading memory efficiency for increased per-user compute costs, creating a choice between serving long contexts or many users.

## Key Takeaways

- **Recognize the memory-compute tradeoff**: Test-time training reduces KV-cache memory requirements from linear to flat growth, but requires serving separate model instances per user, increasing infrastructure costs—only viable for use cases where personalization justifies the expense.
- **Prioritize personalization ROI**: Deploy test-time trained models for sticky, long-session use cases like coding agents that learn codebase conventions, but use shared frozen models for one-off queries where personalization adds no lock-in value.
- **Leverage inference speed gains**: Test-time training can deliver up to 2.7x faster inference on small models with constant latency regardless of context length, enabling new performance-sensitive applications.
- **Plan for divergent model architectures**: As models learn individually per user, infrastructure shifts from serving one shared checkpoint to millions of slightly different models—prepare systems for managing this divergence at scale.

## Related

- [[2026-08-24 How Long Should an AI Agent Live]]
- [[2026-06-25 Full Sail on Asynchronous Inference]]
- [[2026-06-29 When AI Costs More Than the Engineer]]
