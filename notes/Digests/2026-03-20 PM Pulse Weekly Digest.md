# PM Pulse: Weekly Digest — Mar 20, 2026

22 articles from 10 feeds | Mar 13 – Mar 20, 2026

---

## This Week

**Agents are no longer theoretical—they're the operating system for enterprise software, and PMs must decide whether to build them, integrate them, or risk irrelevance.**

This week crystallizes a fundamental shift: AI has moved from isolated automation tools to agentic systems that coordinate across your entire product stack. Three threads dominate: first, agents require PMs to rethink product architecture around autonomy and trust (Edra, OpenClaw, self-improving systems); second, speed and iteration loops trump raw model power for practical work (local models, tight feedback); third, the economic math is forcing a reckoning—hyperscalers are betting $575B that inference demand will explode, but that only happens if agents become embedded in enterprise workflows at scale. For a VP of Product, the tension is acute: you must now evaluate whether your competitive moat depends on agent integration, whether your team can ship agentic features faster than competitors, and how to position retention and expansion around autonomous systems that reduce user friction but demand new accountability models.

- Agents are shifting from novelty to infrastructure—PMs need frameworks for embedding autonomy into existing workflows, not just bolting on AI features.
- Speed and feedback loops now matter more than model size—local, smaller models that enable rapid iteration are outperforming frontier models in production.
- Enterprise adoption hinges on knowledge base automation, not manual integration—companies that can ingest messy internal data without requiring documentation will win.
- Liability and accountability for AI agents are becoming regulatory and operational imperatives—your org design and feature deployment must now account for agent failure modes.

---

## Must-Read

### 1. [Partnering with Edra: Context for Agents at Scale](https://sequoiacap.com/article/partnering-with-edra-context-for-agents-at-scale/)
*Sequoia Capital* — Sequoia Capital — Mar 18, 2026  `#Enterprise`  `#Agentic`  `#Product Growth`

Edra solves a critical enterprise adoption problem by automatically building dynamic knowledge bases from existing company data (tickets, emails, logs, chat) rather than requiring manual documentation. This addresses the core reason most AI agents fail in enterprise: they lack context. As a VP of Product in B2B SaaS, understanding how to enable your customers (or your own team) to operationalize agents at scale without massive data prep is essential for competitive positioning. This is not a feature—it's a foundational shift in how enterprise software will be built and sold.

**Why it matters**: Directly addresses the enterprise AI adoption blocker—knowledge base automation is the missing link between agent capability and production deployment.

- **Eliminate manual documentation burden** by leveraging existing enterprise data sources like support tickets, emails, and chat histories to automatically create transparent, editable knowledge bases that reflect actual business processes.
- **Accelerate agent deployment** in high-pain, data-rich environments first—Edra's early wins focus on IT service management and customer technical support where the ROI is most immediate and measurable.
- **Prioritize transparency over black-box solutions** by choosing AI context systems that allow you to see exactly what the system has learned and why, enabling trust and auditability in enterprise deployments.
- **Invest in founding teams with complementary superpowers**—Eugen's commercial trust-building paired with Yannis's technical excellence creates a dynamic that can tackle complex, skeptical enterprise buyers.

[Read article →](https://sequoiacap.com/article/partnering-with-edra-context-for-agents-at-scale/)

---

### 2. [The Complete Guide to OpenClaw for PMs [EXCLUSIVE]](https://www.news.aakashg.com/p/naman-pandey2-podcast)
*Product Growth* — Aakash Gupta — Mar 17, 2026  `#AI Tools`  `#Org Design`  `#Agentic`

OpenClaw represents a new category of AI tooling that moves beyond reactive language models to proactive agents that can execute scheduled tasks, access local files, and integrate with existing software like Slack. The guide maps five concrete PM use cases (automated competitive intelligence, customer feedback analysis, smart bug routing) that can meaningfully compress operational cycles. For a VP of Product scaling a Series C company, this is immediately relevant: understanding how to deploy agentic tools across your org reduces team friction, accelerates decision-making, and creates a template for selling similar capabilities into your customer base.

**Why it matters**: Practical PM framework for operationalizing AI agents in real workflows; directly applicable to scaling your own product org and customer-facing automation.

- **Install OpenClaw in three commands**: Use npm install, run the onboarding wizard, and hatch your bot—the setup takes 15 minutes and is the barrier most users fail to overcome.
- **Connect to Slack for maximum leverage**: Configure Socket Mode and bot token scopes to embed your AI agent directly into Slack, enabling it to monitor channels, generate reports, and post summaries automatically.
- **Choose model-agnostic LLM providers strategically**: Use Claude Opus for deep research, Gemini Flash for speed, or budget options like Qwen 3.5 depending on the specific use case rather than being locked into one provider.
- **Build persistent automations with cron jobs**: Unlike reactive chatbots, OpenClaw executes scheduled tasks (like 3 a.m. competitive intelligence scans) and maintains growing local repositories of product docs and customer feedback.
- **Understand the workspace file system**: Edit markdown files (soul.md, agents.md, heartbeat.md) to customize bot personality, define operational rules, and configure scheduled automations that persist across restarts.

[Read article →](https://www.news.aakashg.com/p/naman-pandey2-podcast)

---

### 3. [What I Learned Building a Self-Improving Agentic System with Claude](https://www.productcompass.pm/p/self-improving-claude-system)
*Product Compass* — Pawel Huryn — Mar 16, 2026  `#Agentic`  `#Metrics`  `#Product Growth`

The author demonstrates a structured, file-based architecture for building self-improving agentic systems with Claude that compound knowledge over time—enabling rapid content creation, customer research, and competitive intelligence. The system generated 5.2M impressions in three months by treating AI not as a replacement for judgment but as a knowledge-amplification layer. For a VP of Product, this is valuable because it shows how to architect agentic systems that maintain human oversight while scaling operational capacity, and it provides a replicable model for building similar systems within your own team or customer workflows.

**Why it matters**: Demonstrates how to operationalize self-improving systems within a product org; shows the practical architecture for scaling insights and content generation.

- **Structure your Claude knowledge as a file-based graph** with progressive disclosure (CLAUDE.md as brain, INDEX.md as router, subfolders for domains like craft/, voice/, platforms/) so the system only loads relevant context and compounds over repeated use.
- **Delegate execution to AI, retain judgment for humans** — Claude handles research, verification, and pattern-matching while you decide what to post, what to cut, and which angles matter; this split makes taste and judgment more valuable than ever.
- **Test hypotheses with real data and maintain false beliefs documentation** — track what conventional wisdom says fails but your data shows succeeds; one CLAUDE.md instruction can make Claude autonomously propose improvements to its own knowledge base.
- **Apply the same architecture across domains** — replace content labels (craft/, voice/, platforms/) with discovery/, stakeholders/, channels/ for PM research; the pattern works for customer interviews, competitive monitoring, and market intelligence.
- **Start immediately during 2x usage period through March 27** — double usage limits on weekdays and weekends make it the optimal time to begin building compounding systems before returning to normal constraints.

[Read article →](https://www.productcompass.pm/p/self-improving-claude-system)

---

## All Articles

**4.** [PM's Guide to Karpathy's Autoresearch](https://www.news.aakashg.com/p/autoresearch-guide-for-pms) — *Product Growth* · Mar 20, 2026  `#AI Strategy`  `#Roadmapping`  `#Metrics`

Autoresearch is a pattern for autonomously iterating on and optimizing any measurable system (prompts, skills, code) by running hundreds of experimental rounds overnight, and PMs can apply this beyond ML by defining clear metrics and using coding agents to automate the optimization loop.

- **Define a clear numeric metric** for what you want to optimize—replace subjective judgments like 'Is this good?' with measurable yes/no criteria that can be scored programmatically across test runs.
- **Build an evaluation script that runs autonomously** using Claude Code or similar agents so the feedback loop runs without human intervention, enabling dozens of experiments to complete overnight.
- **Isolate the single file the agent can modify** (your prompt, skill, or system instruction) while keeping everything else read-only, preventing the agent from gaming the metric instead of genuinely improving performance.
- **Apply autoresearch to any skill stuck at 70-80% accuracy** by setting up the three-part structure: measurable metric + autonomous eval tool + single editable file, which unlocks 50+ iterations you'd never manually complete.
- **Use the experiment log as your primary artifact**, not just the final result—the log shows you what changes the agent discovered, which often reveals bugs or insights in your original implementation.

**5.** [You Are Responsible for Your Agent](https://www.tomtunguz.com/you-are-responsible-your-agent/) — *Tomasz Tunguz* · Mar 15, 2026  `#Enterprise`  `#Agentic`  `#Leadership`

Companies will soon face significant liability for AI agents used by employees, as regulatory frameworks establish clear accountability and real-world incidents demonstrate the risks of unchecked AI systems in production environments.

- **Establish mandatory governance frameworks** for all agent usage in your organization, including multi-person review processes and safety protocols before agents can access production systems or sign contracts.
- **Assume full organizational liability** for any agent mistakes—whether deployed by employees, contractors, or brought from personal use—as legal precedent shifts responsibility to the company rather than the tool creators.
- **Implement role-based agent access controls** similar to device management policies, restricting which agents can perform critical functions like code deployment, contract signing, and financial transactions.
- **Prepare for regulatory compliance requirements** under emerging AI liability laws like the TRUMP AMERICA AI Act and Utah's AI Policy Act that eliminate the hallucination defense and create pathways for private lawsuits.
- **Audit AI-generated code outputs rigorously** since agent-generated code produces 70% more issues than human-written code, requiring enhanced testing and validation before deployment.

**6.** [Agents Over Bubbles](https://stratechery.com/2026/agents-over-bubbles/) — *Stratechery* · Mar 16, 2026  `#Market Trends`  `#Agentic`  `#Competitive Strategy`

Thompson argues we are not in an AI bubble, but rather at an inflection point where agents—autonomous systems that direct models, verify results, and use deterministic tools—represent a fundamental paradigm shift that justifies massive computing investments and will drive substantially increased demand for inference.

- **Recognize three LLM paradigms**: ChatGPT (initial capability), o1 (reasoning), and agents with harnesses (autonomous task completion) represent distinct inflection points that each dramatically increased compute requirements and practical utility.
- **Agents solve the agency problem**: The historical barrier to AI adoption wasn't capability but user initiative; agents eliminate the need for humans to proactively guide models and verify outputs, making AI adoption exponentially easier.
- **Compute constraints validate investment**: The shift to agentic workloads requiring multiple model calls, CPU resources for agent operations, and continuous use means hyperscaler capex spending is justified by actual demand, not speculation.
- **Infrastructure follows capability**: As agents become the dominant interaction paradigm, the real battleground moves from model weights to the harnesses, tools, and verification systems that make autonomous task completion reliable and scalable.

**7.** [The Robotic Tortoise & the Robotic Hare](https://www.tomtunguz.com/local-vs-cloud-speed/) — *Tomasz Tunguz* · Mar 18, 2026  `#AI Strategy`  `#Competitive Strategy`  `#Metrics`

A local AI model (Qwen 35B) outperformed the more powerful Claude Opus 4.5 in building a payment app by completing the task 3x faster, enabling multiple revision cycles within the same timeframe and demonstrating that speed and tight feedback loops can trump raw intelligence for everyday coding tasks.

- **Prioritize response speed** over model size for iterative development tasks; faster models enable more feedback cycles and refinement rounds before attention or meeting time runs out.
- **Enable tighter feedback loops** in your development workflow by using faster local models for everyday tasks, which can produce better cumulative outcomes through rapid iteration.
- **Match model selection to use case** rather than defaulting to the largest model; complex codebases and agentic workflows may benefit from slower, more powerful models, while rapid prototyping favors speed.

**8.** [The 12x Bet on AI](https://www.tomtunguz.com/blog_post/) — *Tomasz Tunguz* · Mar 17, 2026  `#Market Trends`  `#Competitive Strategy`  `#Agentic`

Hyperscalers are spending $575 billion on AI infrastructure in 2026 while earning only $35 billion in AI revenue today, effectively betting that AI revenue will grow 5-8x within five years to justify this massive capital expenditure and debt issuance.

- **Monitor depreciation schedules** - Hyperscaler asset depreciation timelines (5 years vs. 3 years) reveal their underlying revenue growth assumptions and signal confidence levels in AI monetization.
- **Track capital intensity ratios** - The 12:1 capex-to-revenue ratio ($575B spend on $35B revenue) represents an unprecedented bet; watch if this ratio improves or deteriorates quarterly as a leading indicator of AI ROI realization.
- **Assess debt sustainability** - $159 billion in bonds issued in 2026 alone, with hyperscalers allocating 90% of operating cash flow to AI capex, means any slowdown in AI revenue growth could trigger a debt crisis.
- **Evaluate architectural obsolescence risk** - Nvidia's 12-month GPU release cycle could compress infrastructure useful life from 5 to 3 years, increasing required annual revenue to $276B and making current capex allocations potentially stranded.
- **Benchmark against historical precedent** - The first century bond issued by a tech company since Motorola (1997) signals extreme confidence; compare this to other historical tech infrastructure booms to assess bubble risk.

**9.** [Jensen Huang and Andy Grove, Groq LPUs and Vera CPUs, Hotel California](https://stratechery.com/2026/jensen-huang-and-andy-grove-groq-lpus-and-vera-cpus-hotel-california/) — *Stratechery* · Mar 18, 2026  `#Competitive Strategy`  `#Platform Strategy`  `#Market Trends`

Nvidia is shifting from a single-GPU focused strategy to selling multiple architectures (including competing technologies like Groq LPUs and Vera CPUs) to serve diverse customer needs and maintain market dominance, marking a strategic inflection point at GTC 2026.

- **Diversify your architecture portfolio** to serve different use cases and customer segments rather than forcing all users into a single solution, reducing the risk of disruption from specialized competitors.
- **Study Andy Grove's strategic principles** about maintaining market dominance by evolving your offerings—Nvidia is following the playbook of adapting rather than getting disrupted by new technologies.
- **Recognize the 'Hotel California' trap** where market leaders must continuously innovate and expand offerings to keep customers locked in, or risk losing them to nimble competitors with focused solutions.
- **Monitor inflection points in your industry** where category leaders shift from single-product dominance to multi-architecture strategies, as this signals market maturation and increased competition.

**10.** [An Interview with Nvidia CEO Jensen Huang About Accelerated Computing](https://stratechery.com/2026/an-interview-with-nvidia-ceo-jensen-huang-about-accelerated-computing/) — *Stratechery* · Mar 17, 2026  `#Competitive Strategy`  `#Platform Strategy`

Jensen Huang discusses Nvidia's evolution from a GPU chip company to a full-stack accelerated computing provider, explaining how the company's CUDA ecosystem approach—previously applied to specific industries—now extends to accelerating all software for AI agents to use efficiently.

- **Reframe your value proposition**: Nvidia is repositioning itself not as a chip company but as a full-stack systems integrator, recognizing that $50-60B AI factories require end-to-end solutions including networking, storage, CPUs, and software—not just accelerators.
- **Accelerate existing tools for AI**: Focus on making all enterprise software (Excel, databases, design tools) AI-optimized by applying the same CUDA acceleration approach that worked for specific industries, enabling AI agents to use these tools at machine speed.
- **Own the entire stack to avoid commoditization**: Vertically integrate across power, chips, infrastructure, and software to prevent being squeezed into a single layer of the value chain and to maintain leverage with customers making massive infrastructure investments.
- **Collaborate systemically to optimize**: Move from over-designed siloed systems to coordinated team approaches that push throughput limits and reduce redundancy, delivering better economics and performance in AI infrastructure buildouts.

**11.** [5 of my favorite new retention techniques that you may not have tried](https://www.elenaverna.com/p/5-of-my-favorite-new-retention-techniques) — *Elena's Growth Scoop* · Mar 17, 2026  `#PLG`  `#Product Growth`  `#Metrics`

Elena Verna shares five innovative retention techniques recently tested at Lovable that yielded meaningful improvements, including lite plans in cancellation flows, in-app payment failure notifications, daily free credits, credit rollover policies, and strategic re-engagement campaigns.

- **Create a lite plan option** in your cancellation flow to retain users who no longer need full functionality—Lovable's $5/month lite plan achieved ~10% take rate while improving net retention through renewals.
- **Add in-product payment failure alerts** alongside email notifications to recover involuntary churn—Lovable saw a 50% relative improvement in recovery rate by notifying users in-app when payments fail.
- **Implement daily free credit allowances** for all users (paid and free) to maintain engagement and reduce abandonment from hitting usage limits, particularly effective for AI-based products.
- **Allow credit rollovers for active subscribers** to accommodate bursty usage patterns and increase product likability, which paradoxically improves retention as users accumulate credits they want to use.
- **Use strategic re-engagement campaigns** with personalized messaging based on user activity segments to trigger dormant users—test different messaging angles and measure incrementality to optimize your approach.

**12.** [🎙️ This week on How I AI: From Figma to Claude Code and back & From journalist to iOS developer](https://www.lennysnewsletter.com/p/this-week-on-how-i-ai-from-figma) — *Lenny's Newsletter* · Mar 16, 2026  `#Dev Tools`  `#Design`  `#Agentic`

This episode features two workflow deep-dives: Figma's team demonstrates how to create a bidirectional sync between design and code using Claude Code and MCPs, while LinkedIn's Editor-in-Chief shows how to build iOS apps using a dual-agent system without writing code himself.

- **Eliminate design handoff friction** by implementing bidirectional sync between Figma and production code using MCPs, allowing designers to pull live interfaces, edit them, and push changes back automatically.
- **Prioritize direct manipulation over AI prompting** for precise design adjustments—use visual tools like color pickers in Figma rather than relying on AI to generate exact specifications like hex codes.
- **Invest 20-30% of engineering time optimizing code structure** specifically for AI legibility, ensuring your codebase is readable to AI agents so each prompt delivers better results with less iteration.
- **Automate routine engineering tasks with custom skills** like a `/ship` pre-flight check that validates code, pushes to Git, monitors CI, and fixes minor issues automatically before merge.
- **Create checks-and-balances with dual AI agents**—assign one agent to generate code and another to review for security and architecture, mirroring how human engineering teams create accountability.

**13.** [From journalist to iOS developer: How LinkedIn’s editor builds with Claude Code | Daniel Roth](https://www.lennysnewsletter.com/p/from-journalist-to-ios-developer) — *Lenny's Newsletter* · Mar 16, 2026  `#Dev Tools`  `#Org Design`  `#Agentic`

LinkedIn's editor-in-chief Daniel Roth demonstrates how non-technical professionals can build and ship production-ready iOS apps using Claude Code, employing a dual-agent system and treating AI development like managing a team rather than coding solo.

- **Implement a dual-agent system** with a builder and reviewer agent (Bob and Ray) to catch errors, maintain code quality, and create accountability in AI-assisted development workflows.
- **Adopt a 'picky customer' mindset** rather than trying to understand technical details—focus on what you want the product to do and let Claude handle implementation while you manage priorities.
- **Use branch-based development** and save everything as Markdown files to maintain long-term context and enable iterative improvements without losing your development history.
- **Prioritize features using AI-ranked impact vs. build time** to make data-driven decisions about what to ship next, rather than relying on intuition alone.
- **Ship to production incrementally** by learning the process (App Store submission, Xcode testing) even when AI writes the code, ensuring you understand enough to maintain and improve your product.

**14.** [How I built LennyRPG](https://www.lennysnewsletter.com/p/how-i-built-lennyrpg-f85) — *Lenny's Newsletter* · Mar 17, 2026  `#AI Tools`  `#Product Growth`  `#Design`

Ben Shih, a designer at Miro, shares his step-by-step process for building LennyRPG, a Pokémon-style game based on Lenny's Podcast transcripts, demonstrating how to use AI tools effectively to build visual products from ideation through deployment.

- **Invest in visualization first** – For visually heavy products, sketch out concepts before building so AI can better understand requirements and generate more accurate implementations.
- **Use AI to interview you on your PRD** – Instead of writing requirements from scratch, let Claude or ChatGPT ask clarifying questions to extract the full vision, ensuring the AI has complete context for execution.
- **Follow a structured AI-native build workflow** – Define core idea → Create PRD → Build proof of concept → Add features → Polish → Ship, spending 80% of effort on the first two steps for smoother execution.
- **Validate content generation workflows early** – Test your prompt engineering and content generation (like avatar creation) at the visualization stage to understand what's possible before full implementation.

**15.** [Technical leaders make these 4 common storytelling mistakes](https://newsletter.weskao.com/p/technical-leaders-make-these-4-common) — *Wes Kao* · Mar 18, 2026  `#Leadership`  `#Org Design`

Technical leaders often undermine their storytelling by overloading audiences with technical details, trying to remember too many tactics, including excessive backstory, and attempting overly long narratives. Instead, they should simplify their stories, stay present to elicit emotional investment, cut unnecessary context, and focus on short, impactful anecdotes that can be delivered in 5-15 seconds.

- **Simplify ruthlessly**: Remove technical caveats and tangential details that weigh down your narrative. Focus on hooking your audience to get them in the door, then answer detailed questions afterward.
- **Stay present over rehearsed**: Don't try to remember a checklist of storytelling tactics during delivery. Instead, focus on the "ELU" moment—looking for when your audience's eyes light up with emotional investment.
- **Cut backstory aggressively**: Start your story at the most dramatic or relevant moment, not at the planning phase. Remove 50%+ of what you think is necessary context.
- **Keep stories short by default**: Most leaders should aim for 5-15 second anecdotes rather than full narrative arcs. Unless you're a practiced storyteller, longer stories risk losing your audience and diminishing impact.
- **Use evocative vocabulary**: Paint pictures with visual language and quick anecdotes instead of attempting complex multi-step story structures. This approach is faster, easier to execute well, and delivers the same positive outcomes.

**16.** [“My one big tip for any of these business side roles is you still need to get close to the product. Nothing bothers me more than people that work at companies and never use their own products.” Zapier’s Corp Dev Lead Austin Johnsen on how AI is changing his job and building his own tools with Claude.](https://hunterwalk.com/2026/03/17/my-one-big-tip-for-any-of-these-business-side-roles-is-you-still-need-to-get-close-to-the-product-nothing-bothers-me-more-than-people-that-work-at-companies-and-never-use-their-own-products-zapi/) — *Hunter Walk* · Mar 17, 2026  `#Leadership`  `#Org Design`

Austin Johnsen, Zapier's Corp Dev Lead, shares how AI tools like Claude Code have enabled him to build sophisticated automation systems despite having no engineering background, and emphasizes that business professionals must deeply understand their company's product to be effective.

- **Get close to the product** - Business side employees must actively use their own company's products and develop technical fluency to earn engineer trust and make better decisions, regardless of their background.
- **Start with one problem, iterate** - Build AI tools incrementally by solving individual workflow problems first, which naturally reveals the next automation opportunity and creates momentum.
- **Speed unlocks ambition** - AI reduces friction from ideation to execution so dramatically that non-technical people can attempt projects previously requiring weeks of specialized work, changing what feels feasible to attempt.
- **Breaking into Corp Dev requires existing reps** - Corp Dev roles are rare and high-pressure with little training time available, so target business development or finance roles at high-growth companies instead, where you can operate above your title.
- **AI iteration beats perfection** - Focus on AI tools' speed to correct and improve outputs rather than obsessing over hallucinations; human analysis is also imperfect, but AI can iterate a million times faster.

**17.** [The AI Signal to Noise Curve](https://www.caseyaccidental.com/p/the-ai-signal-to-noise-curve) — *Casey Accidental* · Mar 17, 2026  `#AI Strategy`  `#Roadmapping`  `#Leadership`

The article argues that AI adoption should be strategic rather than comprehensive, with individuals deciding whether to be innovators, early adopters, or mainstream users based on job requirements, rather than trying to keep up with all AI developments. Meaningful AI capability changes happen a few times per year; most weekly noise is irrelevant to your specific role.

- **Assess your role requirements**: Determine if you need to be an innovator, early adopter, or mainstream user based on your job responsibilities—don't pursue mastery in AI areas irrelevant to your core function.
- **Adopt variable positioning**: Sit at different places on the signal-to-noise curve for different AI tools; you can be an innovator in one domain, an early adopter in another, and mainstream in the rest.
- **Filter aggressively based on job impact**: Ignore weekly AI noise and focus only on capabilities that directly serve your job strategy—wait for mainstream adoption if a tool isn't currently required.
- **Distinguish signals from noise**: Meaningful AI capability changes occur only a few times per year; weekly activity on social media is mostly noise, not fundamental shifts worth your attention.

**18.** [🧠 Community Wisdom: Getting a skeptical CTO to adopt AI coding tools, staying after losing faith in the founder, Claude skills for designers, making the most of a jack-of-all-trades role, and more](https://www.lennysnewsletter.com/p/community-wisdom-getting-a-skeptical) — *Lenny's Newsletter* · Mar 14, 2026  `#Org Design`  `#Leadership`  `#Hiring`

This Community Wisdom edition compiles practical advice from Lenny's Slack community on navigating challenges like convincing skeptical CTOs to adopt AI coding tools, managing career decisions after losing faith in founders, and maximizing impact in jack-of-all-trades roles.

- **Start with small wins** when introducing AI coding tools to skeptical CTOs—begin with low-risk, high-impact use cases to build credibility before expanding adoption.
- **Evaluate founder alignment regularly** and establish clear decision criteria before joining or staying with a startup to make objective career choices when faith wavers.
- **Leverage your versatility** as a jack-of-all-trades by identifying which of your skills create the most leverage for your team and double down on those areas.
- **Build Claude skills for design workflows** to streamline creative processes and improve collaboration between design and engineering teams.

**19.** [“If they raise VC, they usually get stuck and it’s a bad outcome for an otherwise good company.” Brad Hargreaves on which proptech companies should seek (or avoid) venture dollars. And more, from the founder of General Assembly, Common, and now, Thesis Driven.](https://hunterwalk.com/2026/03/19/if-they-raise-vc-they-usually-get-stuck-and-its-a-bad-outcome-for-an-otherwise-good-company-brad-hargreaves-on-which-proptech-companies-should-seek-or-avoid-venture-dollars-and-more/) — *Hunter Walk* · Mar 19, 2026  `#Startups`  `#Positioning`

Brad Hargreaves, founder of General Assembly and Common, discusses why many proptech companies should avoid venture capital funding, explaining that asset management businesses lacking exponential growth potential typically get stuck with VC backing despite being otherwise sound companies.

- **Distinguish business models**: Assess whether your proptech company has genuine technology/software, marketplaces, or data opportunities (suitable for VC) versus asset management (better funded through non-venture sources).
- **Avoid VC mismatches**: If your business can't deliver predictable exponential growth, pursuing venture capital will likely constrain your company rather than accelerate it—seek alternative funding sources instead.
- **Understand the full ecosystem**: Real estate investors must monitor AI adoption, regulatory shifts, demographic trends, capital markets, and cultural preferences simultaneously, not just technology trends.
- **Learn from hype cycles**: Evaluate how venture trendiness affects your industry (coliving faced margin compression from over-funding), and make independent decisions rather than following investor sentiment.

**20.** [The tactical playbook for getting 20-40% more comp (without sounding greedy) | Jacob Warwick (Executive Negotiator)](https://www.lennysnewsletter.com/p/the-tactical-playbook-for-getting-more-comp) — *Lenny's Newsletter* · Mar 15, 2026  `#Leadership`

Executive negotiation coach Jacob Warwick reveals that most professionals leave significant compensation on the table, and by applying collaborative negotiation tactics—starting early and using strategic information gathering—you can realistically secure 20-40% more comp without damaging relationships.

- **Start negotiation early** by treating interviews as discovery calls where you gather information about the company's motivations and budget constraints, rather than waiting until an offer arrives.
- **Use the simple question** 'What's the chance there's a little more here?' to unlock immediate 20% bumps—this soft approach works because it acknowledges constraints while leaving room for movement.
- **Master the comp expectation question** by researching market rates first and framing your number as a range tied to specific value you'll deliver, avoiding anchoring yourself too low.
- **Treat job search like enterprise sales** by understanding the hiring manager's pain points, constraints, and what they care about most—this shifts negotiations from confrontational to collaborative.
- **Time your negotiation leverage** by recognizing that information combined with timing creates power; use competing offers and your unique value proposition to justify larger bumps without sounding greedy.

**21.** [Can You Be Part of the System Without Also Being Part of the Problem? Yes but…](https://hunterwalk.com/2026/03/15/can-you-be-part-of-the-system-without-also-being-part-of-the-problem-yes-but/) — *Hunter Walk* · Mar 15, 2026  `#Leadership`

Hunter Walk explores whether one can participate in the tech industry system without perpetuating its problems, concluding 'Yes, but...' with specific conditions like maintaining core beliefs, understanding systemic incentives, and preserving identity outside the system.

- **Maintain first principles dialogue** with people outside your system whom you respect—actively listen to opposing viewpoints and remain open to being wrong about your perspective.
- **Understand the physics of incentives** that drive system behavior—recognize how defaults shape decisions and explicitly identify which incentives you want to limit, counter, or reject, accounting for the costs.
- **Build identity and relationships independent of your industry** through hobbies, family, and communities that aren't tied to your job or cap table to reduce pressure to conform.
- **Opt out of specific systems strategically**—make concrete choices (like leaving Twitter or designing investment structures like Screendoor) that signal your values and limit your participation in problematic mechanics.
- **Acknowledge the risk of rationalization**—remain vigilant about whether your framework justifies staying comfortable rather than creating meaningful change, inviting external scrutiny.

**22.** [Spring Break](https://stratechery.com/2026/spring-break/) — *Stratechery* · Mar 19, 2026

Ben Thompson announces a disjointed Spring Break schedule with no updates on March 19, March 23-24, and March 30, with regular posting resuming March 31, while all other Stratechery Plus content including podcasts remains on schedule.

- **Plan around content gaps** - Note the specific dates when Stratechery updates will not be published (March 19, 23-24, 30) to adjust your reading schedule accordingly.
- **Maintain podcast consumption** - All Stratechery Plus podcasts continue on their regular schedule despite the spread-out break, so audio content remains available.
- **Expect interview content mid-break** - Updates and interviews will resume Wednesday-Thursday March 25-26, providing mid-break content between the gaps.


## Trending on GitHub

**[NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw)** (⭐ 14,031 · JavaScript)
NVIDIA plugin for secure installation of OpenClaw
*NVIDIA's secure OpenClaw plugin signals enterprise focus on AI infrastructure security—critical as you integrate AI into production systems.*

**[aiming-lab/AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw)** (⭐ 7,028 · Python)
Fully autonomous & self-evolving research from idea to paper. Chat an Idea. Get a Paper. 🦞
*Autonomous research-to-paper generation shows AI agents handling complex workflows end-to-end; consider similar automation opportunities in your product.*

**[calesthio/Crucix](https://github.com/calesthio/Crucix)** (⭐ 5,482 · JavaScript)
Your personal intelligence agent. Watches the world from multiple data sources and pings you when something changes.
*Personal intelligence agents monitoring multiple data sources represent emerging product pattern—real-time alerts and multi-source aggregation users now expect.*

**[jackwener/opencli](https://github.com/jackwener/opencli)** (⭐ 2,863 · TypeScript)
Make any website your CLI. A powerful, AI-native runtime for seamless browser automation and dynamic web data extraction.
*AI-native CLI tools for website automation indicate rising demand for no-code/low-code data extraction—evaluate if your platform needs similar capabilities.*

**[MoonshotAI/Attention-Residuals](https://github.com/MoonshotAI/Attention-Residuals)** (⭐ 2,123 · N/A)
No description
*Attention residuals research suggests optimization breakthroughs in model efficiency; monitor for architectural improvements affecting AI product performance and costs.*


## Trending on Hacker News

**[Polymarket gamblers threaten to kill me over Iran missile story](https://www.timesofisrael.com/gamblers-trying-to-win-a-bet-on-polymarket-are-vowing-to-kill-me-if-i-dont-rewrite-an-iran-missile-story/)** (▲ 1,600 · 💬 1,052) — [discussion](https://news.ycombinator.com/item?id=47397822)
*Market prediction platform risks highlight regulatory and safety challenges as AI-driven decision-making reaches mainstream—ensure your product has appropriate guardrails.*

**[Kagi Translate now supports LinkedIn Speak as an output language](https://translate.kagi.com/?from=en&to=LinkedIn+speak)** (▲ 1,454 · 💬 339) — [discussion](https://news.ycombinator.com/item?id=47408703)
*Translation feature parity across platforms shows feature expectations rising; consider multilingual output and integration breadth as competitive requirements.*

**[Astral to Join OpenAI](https://astral.sh/blog/openai)** (▲ 1,408 · 💬 857) — [discussion](https://news.ycombinator.com/item?id=47438723)
*Astral joining OpenAI signals ecosystem consolidation and indicates where talent and innovation are concentrating—watch for platform shifts affecting your roadmap.*

**[Palestinian boy, 12, describes how Israeli forces killed his family in car](https://www.bbc.com/news/articles/c70n2x7p22do)** (▲ 1,249 · 💬 410) — [discussion](https://news.ycombinator.com/item?id=47402950)
*Geopolitical content moderation challenges underscore the content governance complexity growing products face—factor safety and trust into your scaling plans.*

**[1M context is now generally available for Opus 4.6 and Sonnet 4.6](https://claude.com/blog/1m-context-ga)** (▲ 1,219 · 💬 519) — [discussion](https://news.ycombinator.com/item?id=47367129)
*Massive context windows (1M tokens) enable new use cases like document analysis and long-form reasoning; evaluate whether longer context unlocks product differentiation.*

