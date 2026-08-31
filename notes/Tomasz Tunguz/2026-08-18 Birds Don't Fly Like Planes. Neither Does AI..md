# Birds Don't Fly Like Planes. Neither Does AI.

**Source**: [Tomasz Tunguz](https://tomtunguz.com/birds-dont-fly-like-planes-neither-does-ai/)
**Author**: Tomasz Tunguz | **Date**: Aug 18, 2026

---

## Summary

Smaller local AI models can achieve identical quality to larger cloud models by using different reasoning strategies—they think longer but skip unnecessary steps, similar to how bumblebees and hummingbirds fly differently than planes despite reaching the same destination.

## Key Takeaways

- **Measure end-to-end latency, not token speed.** A model generating 2.2x faster tokens can still finish slower overall if it requires 3.1x more thinking tokens; focus on time-to-answer rather than throughput metrics.
- **Deploy smaller models locally for cost-effective performance.** A 27B-parameter local model can match the quality of frontier 753B cloud models by trading inference-time compute for capability, making on-device deployment viable.
- **Understand model reasoning patterns to optimize deployment.** Smaller models deliberate internally with chain-of-thought reasoning while larger models skip directly to answers; choose deployment based on your latency vs. cost tradeoff, not raw capability rankings.

## Related

- [[2026-08-17 When Models Learn]]
- [[2026-06-29 When AI Costs More Than the Engineer]]
- [[2026-07-20 Open Models Tack Toward the Frontier]]
