# Weekly PM Digest — Mar 07, 2026

29 articles from 14 feeds | Feb 28 – Mar 07, 2026

---

## Must-Read

### 1. [Services: The New Software](https://sequoiacap.com/article/services-the-new-software/)
*Sequoia Capital* — Sequoia Capital (featuring Julien Bek) — Mar 06, 2026

Sequoia argues the next trillion-dollar company will be a services firm powered by AI, not a software tool company, because AI makes services faster/cheaper while commoditizing tools. For a Series C SaaS startup, this suggests a critical strategic choice: build proprietary AI capabilities that deliver outcomes (services) rather than compete on feature parity. The path forward involves replacing outsourced work with AI autopilots, then expanding to judgment-heavy tasks as your models gain proprietary data advantages—fundamentally reshaping how to think about product-market fit and competitive moats.

**Why it matters**: Reframes company strategy from software tools to AI-powered services, directly impacting product roadmap and GTM positioning

- **Start with outsourced work**: Target services that companies already outsource (accounting, legal, insurance) because the budget exists, substitution is frictionless, and you can immediately compete on cost and speed.
- **Differentiate on judgment, not intelligence**: Build copilots for intelligence work today, but plan to transition to autopilots by accumulating proprietary data about what good judgment looks like in your domain.
- **Capture the work budget, not the tool budget**: The labor spend in any profession dwarfs software spending by 6:1, so position your AI as an outcome delivery service rather than a productivity tool.
- **Map your vertical on two axes**: Plot your target services market on an intelligence-to-judgment spectrum and outsourced-to-insourced ratio to identify the highest-priority wedge opportunities.
- **Expand from wedge to TAM**: Once you own the outsourced, intelligence-heavy wedge, use accumulated data and trust to move upmarket into insourced, judgment-heavy work where the real long-term value lives.

[Read article →](https://sequoiacap.com/article/services-the-new-software/)

---

### 2. [The PM's Guide to Agent Distribution: MCP Servers, CLIs, and AGENTS.md](https://www.news.aakashg.com/p/master-ai-agent-distribution-channel)
*Product Growth* — Aakash Gupta — Mar 07, 2026

AI agents are becoming the dominant software distribution channel, and product teams must build agent-accessible surfaces (AGENTS.md files, CLIs, MCP servers) or risk invisibility in the fastest-growing software market. This represents a fundamental shift in product strategy: your product discovery won't happen through traditional UI design but through machine-readable interfaces that agents can understand and interact with autonomously. Ignoring this distribution channel means ceding user acquisition and integration opportunities to competitors who ship agent-native features.

**Why it matters**: Defines how AI agents will discover and distribute your product, essential for product visibility and adoption strategy

- **Prioritize API quality first** - Your API is the foundation for all agent-accessible layers; broken authentication or poor design will undermine MCP servers and CLIs.
- **Start with AGENTS.md documentation** - Create machine-readable documentation with executable commands, code examples, and clear boundaries before building CLIs or MCP servers.
- **Build CLIs as composable wrappers** - Develop CLI tools that pipe JSON output and use environment variable auth, which agents can use natively and developers already understand.
- **Invest in high-quality MCP servers** - Write precise tool descriptions, set clear boundaries on capabilities, and test with multiple AI clients to ensure agents reliably select the right tools.
- **Monitor agent-specific metrics** - Track which agent tools agents actually select, measure error rates per tool, and iterate based on agent behavior rather than human usage patterns.

[Read article →](https://www.news.aakashg.com/p/master-ai-agent-distribution-channel)

---

### 3. [WebMCP Explained for Product Teams](https://departmentofproduct.substack.com/p/webmcp-explained-for-product-teams)
*Department of Product* — Rich Holmes — Mar 02, 2026

WebMCP is a new protocol (developed by Google, Microsoft, and W3C) that lets product teams explicitly tell AI agents what features their products offer, rather than forcing agents to reverse-engineer UIs through screenshots. This is a strategic opportunity for your product roadmap: by adopting WebMCP standards, you can ensure agents discover and use your product's capabilities correctly, improve integration outcomes, and potentially capture agent-native workflows before competitors do. This should be on your near-term technical roadmap as a core product integration priority.

**Why it matters**: Provides concrete framework for product teams to control how AI agents interact with their products

- **Implement WebMCP APIs** to make your product's features and tools explicitly discoverable to AI agents in the browser, replacing fragile screenshot-based interaction methods.
- **Take control of AI agent interactions** by defining your product's capabilities directly rather than allowing agents to misinterpret your UI through vision models.
- **Prepare your product now** by understanding the three strategic steps product teams can take immediately to prepare for WebMCP adoption regardless of how the standard evolves.
- **Monitor the early preview program** that Chrome launched in February to gain hands-on experience with WebMCP before it becomes widely adopted.

[Read article →](https://departmentofproduct.substack.com/p/webmcp-explained-for-product-teams)

---

## All Articles

**4.** [Revenue addiction kills companies.](https://www.elenaverna.com/p/revenue-addiction-kills-companies) — *Elena's Growth Scoop* · Mar 06, 2026

Revenue addiction—prioritizing short-term revenue targets above all else—is killing companies by crushing innovation, long-term strategy, and customer focus, making them fatally vulnerable to AI disruption. Instead, companies should treat revenue as an output of delivering customer value, not as the primary north star metric.

- **Shift your North Star metric** away from revenue to a leading indicator like daily active users or customer engagement that naturally drives revenue as a downstream outcome
- **Kill the quarterly pressure cooker** by rejecting arbitrary revenue targets that incentivize dark UX patterns, price gouging, and short-term fixes instead of sustainable growth
- **Protect innovation budgets** by allowing 20-30% of roadmap capacity for long-term strategic bets and risk-taking that won't show revenue impact for 12+ months
- **Build a culture that accepts failure** by decoupling individual performance evaluations from short-term revenue attribution, so teams feel safe proposing creative and risky ideas
- **Track customer satisfaction qualitatively** alongside quantitative metrics (like NPS and value scores) to catch the lagging indicator of customer churn before it becomes irreversible

**5.** [Why Product Sense is the only product skill that will matter in the AI age](https://shreyasdoshi.substack.com/p/why-product-sense-is-the-only-product) — *Shreyas Doshi* · Mar 05, 2026

As AI tools become commoditized and universally accessible, the only sustainable competitive advantage for product leaders will be their ability to apply superior judgment and intuition to improve upon AI-generated insights. This combination of skills—what Doshi calls 'Product Sense'—comprises empathy, simulation ability, strategic thinking, taste, and creative execution.

- **Stop relying on AI tools as career moats**: Learn all available AI tools for near-term advantage, but recognize that tool mastery alone won't differentiate you long-term since competitors will have equal access to equivalent capabilities.
- **Develop Product Sense as your core skill**: Build expertise in the five components—empathy, simulation, strategic thinking, taste, and creative execution—that enable you to improve upon AI outputs rather than merely consume them.
- **Focus on human judgment over technical implementation**: Your value lies in making better decisions about which AI recommendations to accept, reject, or modify based on customer needs, market dynamics, and business strategy.
- **Think independently rather than seeking answers from experts**: Use logic and first principles to develop your own predictions about AI's impact on product work, changing your assumptions when warranted rather than accepting others' conclusions.
- **Build organizational systems around AI feedback loops**: Invest in better data pipelines, customer insight integration, and decision-making workflows that allow you to leverage AI more effectively than competitors.

**6.** [🔵 OpenAI's Engineers have Cloned a SaaS Product](https://departmentofproduct.substack.com/p/openais-engineers-have-cloned-a-saas) — *Department of Product* · Mar 06, 2026

OpenAI engineers have built an in-house GitHub alternative due to productivity frustrations with outages, signaling a potential new trend of tech companies cloning critical SaaS tools. The article explores what this means for product teams and highlights major AI product developments from companies like Google, Anthropic, and emerging design tools.

- **Monitor internal tool creation trends**: When major tech companies like OpenAI build clones of popular SaaS products, it signals potential market gaps or reliability issues that your product team should address to prevent similar defection.
- **Integrate AI agents into your product workflow**: Google's new Workspace Command Line tool enables Claude Code users to automate tasks like pulling feature requests, creating docs, and scanning calendars—consider how AI agent access could enhance your product's capabilities.
- **Adopt multimodal interfaces**: Voice modes are becoming standard across Claude Code and Perplexity; product teams should experiment with voice input and output as a natural interface for user commands and background task execution.
- **Evaluate design tool alternatives**: Paper is challenging Figma's dominance as an AI-native design tool that works directly with code and DOM—product teams should assess emerging alternatives to their current design stack.
- **Prototype rapidly over documentation**: Anthropic's approach of building dozens of prototype versions in days instead of writing PRDs suggests that iterative prototyping with AI tools may be more effective than traditional product documentation processes.

**7.** [How Coinbase scaled AI to 1,000+ engineers | Chintan Turakhia](https://www.lennysnewsletter.com/p/how-coinbase-scaled-ai-to-1000-engineers) — *Lenny's Newsletter* · Mar 02, 2026

Coinbase's Senior Director of Engineering shares how he scaled AI adoption across 1,000+ engineers, achieving dramatic efficiency gains like reducing PR review times from 150 to 15 hours through hands-on leadership and custom AI integration.

- **Demonstrate hands-on expertise**: Engineering leaders must personally use and master AI tools before expecting team adoption, as leadership conviction drives organizational change.
- **Run "speed run" events**: Execute focused sprints like the 100-engineer, 70-PR in 15 minutes challenge to showcase AI's velocity gains and build momentum across the team.
- **Measure the right metrics**: Track actionable engineering velocity indicators like PR review time reduction and feedback-to-ship cycle compression rather than vanity metrics.
- **Build custom AI agents**: Integrate AI into existing workflows through custom Slack bots and tools like Cursor to reduce friction and make adoption seamless.
- **Identify and replicate power user behaviors**: Study how top performers use AI tools and codify their practices into training and standards for the broader organization.

**8.** [Would You Buy Generic AI?](https://www.tomtunguz.com/white-label-ai/) — *Tomasz Tunguz* · Mar 02, 2026

AI models are experiencing a dramatic commoditization similar to generic pharmaceuticals, with Chinese AI labs offering equivalent capabilities to US frontier models at 90% lower costs, compressing the typical product lifecycle from decades to weeks.

- **Monitor pricing compression** across your AI infrastructure costs, as Chinese models like DeepSeek V3 ($0.14/M tokens) undercut GPT-5.2 ($1.75/M tokens) by 12x—audit which vendor APIs you're locked into and identify switching opportunities.
- **Evaluate distillation risks** for proprietary models by implementing prompt injection defenses and monitoring for unauthorized knowledge extraction campaigns targeting your AI systems.
- **Plan for margin erosion** in AI-dependent products by stress-testing unit economics at 50-80% price reductions and diversifying beyond API dependencies into proprietary fine-tuned models or unique data.
- **Accelerate differentiation beyond base models** by building specialized capabilities, RAG systems, and domain-specific training that competitors cannot easily replicate through distillation.

**9.** [TBM 409: Minimally Viable Consistency (Part 2)](https://cutlefish.substack.com/p/tbm-409-minimally-viable-consistency) — *The Beautiful Mess* · Mar 04, 2026

The article explores the challenge of achieving 'minimally viable consistency' in company operating systems—finding the fewest consistent concepts needed to operate effectively while allowing for local variation. It examines how ideas unexpectedly gain traction (Model Market Fit), the complications of strategic shifts, the myth of standardized frameworks, and the tension between organizational consistency and team viability.

- **Embrace Model Market Fit**: Stop trying to force predetermined frameworks and instead observe which ideas naturally gain traction in your organization, then build upon those emergent patterns rather than fighting them.
- **Watch for consistency traps during strategic shifts**: When strategy changes faster than structure, be cautious about introducing 'temporary consistency' measures—they easily become permanent and may mask the real problem (often prioritization, not processes).
- **Invest in fractal rituals over pyramids**: Focus consistency efforts on actionable, repeatable practices like kickoff formats and one-pager templates rather than high-level abstractions like pillars and vision statements that create illusions of alignment.
- **Recognize that framework implementation varies wildly**: Understand that standardized frameworks like OKRs will be interpreted differently across teams; this variation may be a feature, not a bug—decide consciously whether flexibility or consistency serves your context better.
- **Define viability from multiple perspectives**: Acknowledge that what seems viable and valuable to leadership (like mandatory sprint lengths) may create friction for teams doing the actual work; actively seek input from those absorbing the friction points.

**10.** [Gemini Gem Masterclass From the Creator Lisa Huang](https://www.news.aakashg.com/p/lisa-huang-podcast) — *Product Growth* · Mar 05, 2026

The best PMs treat AI as a personalized team member rather than a generic search engine, leveraging tools like Gemini Gems to maintain persistent context about their product, strategy, and communication style. Lisa Huang, SVP of Product at Xero and former AI PM at Google, Meta, and Apple, shares a masterclass on building effective AI features, hardware AI experiences, and navigating the AI PM career path.

- **Build three essential Gems**: Create a writing clone for consistent voice, a product strategy advisor for decision-making support, and a user research synthesizer to surface patterns from customer data.
- **Write detailed instructions and upload context documents**: Treat Gem creation like briefing a new hire with specific role definitions, audience context, and uploaded knowledge files—vague instructions are the biggest failure point.
- **Prioritize user needs over technology capabilities**: The best AI products live at the intersection of what users genuinely need and what technology can reliably deliver today; avoid falling in love with the technology itself.
- **Build AI agents with domain knowledge and proprietary data**: High-stakes domains require understanding specific workflows, accuracy thresholds, and leveraging unique transaction-level data rather than generic LLM outputs.
- **Use hybrid architectures strategically**: Combine LLMs in multi-agent workflows where appropriate but use programmatic code where reliability and control are critical rather than making everything non-deterministic.

**11.** [PM Skills Marketplace: The AI Operating System for Better Product Decisions](https://www.productcompass.pm/p/pm-skills-marketplace-claude) — *Product Compass* · Mar 02, 2026

Pawel Huryn launches the PM Skills Marketplace, an open-source collection of 65 PM skills and 36 chained workflows built on proven frameworks, designed to give PMs structured decision-making tools within Claude Code and Cowork rather than generic AI text outputs.

- **Install the PM Skills Marketplace** via Claude Cowork (recommended for non-developers) or Claude Code CLI by adding phuryn/pm-skills to access all 8 plugins and 65 skills immediately.
- **Use commands to chain workflows together** like /discover (ideation → assumption mapping → prioritization → experiments) to follow proven PM methodologies step-by-step instead of relying on generic AI assistance.
- **Leverage skills automatically or force-load them** with /plugin-name:skill-name syntax to encode domain knowledge from Teresa Torres, Marty Cagan, and Alberto Savoia into your daily PM work.
- **Access 8 specialized plugin domains** covering discovery, strategy, execution, market research, data analytics, marketing/growth, and go-to-market to structure decisions across your full PM toolkit.
- **Build reusable frameworks like Opportunity Solution Trees and metrics dashboards** that multiple commands can reference, creating consistency across discovery, strategy validation, and execution planning.

**12.** [Not Prompts, Blueprints](https://www.tomtunguz.com/filling-the-queue-for-ai/) — *Tomasz Tunguz* · Mar 04, 2026

Rather than micromanaging AI through iterative prompts, effective AI workflows require upfront planning and blueprinting that anticipate decision branches and edge cases, allowing agents to run autonomously in the background.

- **Plan workflows visually** - Sketch out your AI workflow on paper or as images before execution, mapping decision branches and potential edge cases to eliminate back-and-forth prompting.
- **Anticipate failure points** - Identify gaps in advance (missing CRM data, unavailable resources, missing transcripts) rather than discovering them during agent execution.
- **Shift from prompt-response cycles** - Move away from iterative "prompt, response, prompt" patterns toward autonomous agent execution by providing complete blueprints upfront.
- **Use visual workflows as specifications** - Capture workflow diagrams as images that agents can reference, enabling more effective autonomous operation than text-based prompts alone.

**13.** [🎙️ This week on How I AI: 5 OpenClaw agents run my home, finances, and code & How Coinbase scaled AI to 1,000+ engineers](https://www.lennysnewsletter.com/p/this-week-on-how-i-ai-5-openclaw) — *Lenny's Newsletter* · Mar 02, 2026

This episode features two distinct AI implementation stories: Jesse Genet's multi-agent home automation system treating agents like employees with partitioned access, and Coinbase's scaled AI adoption approach that accelerated engineering velocity across 1,000+ engineers.

- **Treat agents as employees** by giving each AI agent a defined role, scoped data access, and progressive trust model rather than full system permissions, inspired by hiring best practices.
- **Use photos as primary agent input** to reduce friction—photograph curriculum, supplies, or physical items and let agents handle structuring, categorizing, and connecting the information without manual data entry.
- **Run speed runs to prove AI ROI** by orchestrating high-visibility events (like Coinbase's 100 engineers shipping 75 PRs in 15 minutes) that demonstrate effectiveness and overcome organizational skepticism.
- **Eliminate soul-sucking work first** by targeting tedious tasks engineers hate (linting, unit tests, Git management) to create immediate buy-in before tackling complex problems.
- **Create decision files to prevent agent re-litigation** of settled choices—maintain a centralized decisions document so agents know which topics are final and shouldn't be revisited.

**14.** [How to debug a team that isn’t working: the Waterline Model](https://www.lennysnewsletter.com/p/how-to-debug-a-team-that-isnt-working) — *Lenny's Newsletter* · Mar 03, 2026

Molly Graham presents the Waterline Model, a diagnostic framework that helps managers identify the true root causes of team underperformance by examining structural and environmental factors before blaming individuals.

- **Avoid the blame trap** by recognizing that jumping to personnel changes is often the wrong first step when diagnosing team problems.
- **Use the Waterline Model layers** systematically to diagnose issues in order, starting with structural factors before examining individual performance.
- **Snorkel before you scuba** by conducting shallow investigations first to understand the full context before making deep organizational or personnel decisions.
- **Recognize rational behavior** in faulty environments—poor performance may reflect reasonable adaptation to broken systems rather than individual capability issues.

**15.** [The design process is dead. Here’s what’s replacing it. | Jenny Wen (head of design at Claude)](https://www.lennysnewsletter.com/p/the-design-process-is-dead) — *Lenny's Newsletter* · Mar 01, 2026

Jenny Wen, head of design at Anthropic/Claude, discusses how the traditional design process of discovery → mock → iterate is becoming obsolete in the AI era, and reveals what's replacing it along with how designers should adapt their skills and workflows.

- **Rethink your design workflow** - The traditional linear design process is dead; designers must now work in parallel with AI tools and iterate based on real user feedback rather than extensive upfront mocking.
- **Build AI-native design skills** - Develop proficiency with AI tool stacks like Claude Code, v0, and other AI-powered design tools to remain competitive as a designer in 2026.
- **Hire for three archetypes** - When building design teams, focus on recruiting against specific archetypes that Jenny identifies as essential for AI-era design work.
- **Understand interface durability** - Chatbot interfaces may be more durable and long-lasting than skeptics expect, so invest in mastering conversational UI design patterns.
- **Move from director to IC impact** - Consider the strategic value of returning to individual contributor work to stay hands-on with emerging design paradigms, as Jenny did leaving Figma for Anthropic.

**16.** [Every Product Starts in Oklahoma](https://www.caseyaccidental.com/p/every-product-starts-in-oklahoma) — *Casey Accidental* · Mar 03, 2026

Products must navigate two distinct customer archetypes—Sooners who adopt early for status and exploration, and Missourians who require proof and financial clarity—and successfully transition from building for one to the other as they scale.

- **Identify your current customer type** by observing whether they're motivated by status/exploration (Sooners) or by financial ROI/risk reduction (Missourians), then build feedback loops accordingly rather than trying to satisfy both simultaneously.
- **Discard Missourian feedback early** in your product development; focus on Sooner engagement as your primary signal of progress, since Missourians won't commit substantively until scale and peer proof exist.
- **Rearchitect your value proposition** as you scale from Sooners to Missourians by converting social capital into financial capital, making transaction economics visible, and shifting from play-based to business-based motivations.
- **Make monetization mechanics transparent** to Missourians through visible economics (ads, fees, percentages), as hidden revenue models create skepticism and reduce adoption in skeptical user segments.

**17.** [Data Center Intelligence at the Price of a Laptop](https://www.tomtunguz.com/qwen-9b-matches-frontier-models/) — *Tomasz Tunguz* · Mar 05, 2026

Frontier-level AI models are now running locally on consumer laptops at a fraction of cloud API costs, fundamentally changing the economics of AI inference and enabling private, unrestricted intelligence work.

- **Calculate your payback period**: A $5,000 laptop with sufficient RAM pays for itself within weeks at moderate usage rates (20M tokens/day), after which marginal costs drop to just electricity.
- **Prioritize privacy and control**: Local inference eliminates API logging, third-party data retention, rate limits, and outage risks—critical for sensitive work like financial research and internal memos.
- **Redesign workflows for latency**: Optimize for sequential depth over parallel breadth by queuing single-threaded tasks to run overnight rather than attempting concurrent agentic workflows.
- **Reassess cloud vendor lock-in**: With 9B open-source models matching December 2025 frontier capabilities, the buy-vs-rent equation has inverted—reconsider which workloads justify ongoing API spending.

**18.** [Anthropic’s Skyrocketing Revenue, A Contract Compromise?, Nvidia Earnings](https://stratechery.com/2026/anthropics-skyrocketing-revenue-a-contract-compromise-nvidia-earnings/) — *Stratechery* · Mar 04, 2026

Anthropic's enterprise business is experiencing rapid revenue growth and reaching critical scale, while the company navigates important government relations and policy compromises. Agent adoption is simultaneously driving massive demand increases for Nvidia chips, reshaping the hardware economics of AI.

- **Monitor Anthropic's revenue trajectory** - The company's enterprise business is reaching escape velocity, signaling a shift from research-focused to revenue-driven operations that will impact competitive dynamics
- **Government relations are critical** - Finding a compromise between Anthropic and government entities is becoming increasingly important as the company scales, affecting regulatory and business outcomes
- **Agent deployment changes chip economics** - Agents dramatically increase demand for Nvidia hardware, creating new opportunities for infrastructure providers even as software capabilities advance

**19.** [Databricks Overtakes Snowflake](https://www.tomtunguz.com/databricks-overtakes-snowflake/) — *Tomasz Tunguz* · Mar 01, 2026

Databricks has overtaken Snowflake in revenue by capitalizing on AI's architectural shift toward unstructured data processing, while Snowflake's historical focus on structured data and SQL queries leaves it playing catch-up in the AI era.

- **Recognize architectural transitions**: AI represents a fundamental architectural shift rather than a feature addition—companies betting on yesterday's data paradigms will struggle to compete as the market evolves.
- **Build for the data that matters now**: Databricks' willingness to handle messy, unstructured data (images, documents, logs, audio) positioned it perfectly for AI training needs, while Snowflake's clean structured data advantage became less relevant.
- **Accelerate growth at scale**: Databricks is growing 65% YoY at $5B+ revenue—a rare achievement that indicates strong product-market fit and the power of riding architectural waves rather than incremental improvements.
- **Diversify beyond core products**: Databricks SQL grew from $100M to $1B in three years, but AI products like Lakebase are growing twice as fast, showing the importance of expanding into emerging use cases early.
- **Move fast in response to threats**: Snowflake's Intelligence product and $200M in AI partnerships show reactive rather than proactive positioning, suggesting that defensive moves after losing architectural momentum are harder to execute successfully.

**20.** [🧠 Community Wisdom: Business books that haven’t aged well, vibe coding with your Figma design systems, Claude Code vs. other coding tools and more](https://www.lennysnewsletter.com/p/community-wisdom-business-books-that) — *Lenny's Newsletter* · Mar 07, 2026

This Community Wisdom edition curates the most insightful subscriber discussions from Lenny's Slack community, covering topics like outdated business book recommendations, Figma design system strategies, and comparisons between Claude Code and alternative coding tools.

- **Reassess your reading list** by identifying which classic business books no longer apply to modern product development and replace them with current frameworks
- **Optimize your design systems** by learning how top PMs leverage Figma to create scalable, maintainable component libraries
- **Evaluate coding tool tradeoffs** by comparing Claude Code against alternatives based on your specific workflow and integration needs
- **Engage with community intelligence** by participating in peer discussions to surface practical insights faster than solo research

**21.** [2026.10: Higher Powers and Lower Macs](https://stratechery.com/2026/higher-powers-and-lower-macs/) — *Stratechery* · Mar 06, 2026

This week's Stratechery roundup covers Anthropic's escalating standoff with the U.S. government over military contracts and alignment concerns, while Apple releases the budget-focused MacBook Neo—marking a rare shift toward affordability rather than premium positioning.

- **Understand the Anthropic paradox**: The company's concerns about military AI alignment are legitimate, but its refusal to work with the government is unrealistic given AI's national security implications—compromise will likely be necessary.
- **Apple's downmarket shift signals strategy change**: The MacBook Neo represents Tim Cook's pragmatic approach to use excess chip production, but it contradicts the premium, thin design philosophy that previously defined Mac positioning.
- **Government-tech tension is historical, not new**: Modern regulatory pressure on AI companies reflects long-established patterns of government leverage on private businesses, not unprecedented overreach—context matters in evaluating current controversies.
- **AI military applications are advancing rapidly**: The state of autonomous weapons and military AI in 2026 has moved beyond theoretical debate into practical deployment questions that require informed policy frameworks.

**22.** [Anthropic and Alignment](https://stratechery.com/2026/anthropic-and-alignment/) — *Stratechery* · Mar 02, 2026

Ben Thompson examines Anthropic's refusal to remove AI safety safeguards for Pentagon use, arguing that unelected private companies shouldn't unilaterally decide military technology capabilities that should be determined by elected government officials.

- **Recognize the power asymmetry**: Private companies like Anthropic lack democratic accountability, yet their refusal to cooperate with elected governments on national security matters raises questions about who should control critical technology decisions.
- **Understand the alignment dilemma**: AI safety concerns are legitimate, but delegating military and surveillance decisions to corporate leadership rather than elected officials creates a governance problem that transcends the technical issues.
- **Consider precedent and consistency**: If Anthropic successfully restricts government use of its models, it establishes a dangerous precedent where private entities can override sovereign government authority on defense matters.
- **Evaluate the real constraints**: The actual barrier to autonomous weapons deployment may not be technical reliability (as Anthropic claims) but rather legitimate policy disagreements about democratic values and oversight mechanisms.

**23.** [An Interview with Gregory Allen About Anthropic and the U.S. Government](https://stratechery.com/2026/an-interview-with-gregory-allen-about-anthropic-and-the-u-s-government/) — *Stratechery* · Mar 05, 2026

Ben Thompson interviews Gregory Allen about Anthropic's ongoing dispute with the U.S. government, exploring the intersection of AI development, national security concerns, and regulatory frameworks.

- **Understand the regulatory landscape**: AI companies operating at the frontier must navigate complex government relationships and national security considerations that go beyond typical commercial business concerns.
- **Monitor policy developments**: The outcome of Anthropic's government dispute will set precedents for how AI companies interact with federal agencies and may shape future AI regulation.
- **Prepare for government engagement**: AI companies need dedicated expertise and strategy for managing relationships with government stakeholders, similar to defense or telecom sectors.

**24.** [Technological Scale and Government Control, Paramount Outbids Netflix for Warner Bros.](https://stratechery.com/2026/technological-scale-and-government-control-paramount-outbids-netflix-for-warner-bros/) — *Stratechery* · Mar 03, 2026

The article examines how government influence and technological scale are reshaping media industry dynamics, illustrated by Paramount's successful bid for Warner Bros. over Netflix, and explores whether Netflix's loss represents strategic relief from an unfavorable acquisition.

- **Recognize that government relationships** are becoming as critical as consumer market share for tech and media companies navigating regulatory environments and scale requirements.
- **Evaluate acquisition strategy beyond pure economics** by considering whether winning bids align with long-term operational complexity and regulatory exposure.
- **Understand scale trade-offs** where larger technological platforms face greater government scrutiny and control considerations that smaller competitors may avoid.

**25.** [50 Lessons From 50 Years Lived](https://debliu.substack.com/p/50-lessons-from-50-years-lived) — *Perspectives (Deb Liu)* · Mar 05, 2026

On her 50th birthday, Deb Liu reflects on five decades of life lessons and shares 50 key insights spanning identity, career, leadership, communication, and relationships that she has learned through personal experience and writing over 250 blog articles.

- **Define your own success metrics** before external pressures do, by writing a personal mission statement to ensure clarity and alignment with your values rather than optimizing for others' goals.
- **Treat your career like a product roadmap** with intentional planning, skill development beyond your current role, and strategic preparation for transitions to unlock sustained growth.
- **Cultivate connections over transactions** in networking, friendships at work, and leadership by prioritizing genuine relationships and common ground rather than purely transactional interactions.
- **Choose an abundance mindset** to uncover possibilities and win-win solutions that scarcity thinking obscures, reshaping how you view obstacles and opportunities.
- **Master change navigation** by recognizing that pivots aren't detours, preparation matters for new roles, and your response to inevitable life transitions determines your trajectory forward.

**26.** [The AI Vampire; Startup Tolan Changes How It Hires Engineers in an AI World; Do You Back Into Parking Spots?; Social Engineer Hacks Against AI Agents; and More++ [link blog]](https://hunterwalk.com/2026/03/01/the-ai-vampire-startup-tolan-changes-how-it-hires-engineers-in-an-ai-world-do-you-back-into-parking-spots-social-engineer-hacks-against-ai-agents-and-more-link-blog/) — *Hunter Walk* · Mar 01, 2026

This curated roundup explores how AI is transforming engineering hiring practices, the extractive nature of AI productivity gains, and emerging security threats like prompt injection attacks targeting AI agents. The collection examines both the opportunities and risks as companies adapt to an AI-native world.

- **Redesign your interview process** to test practical problem-solving skills rather than algorithmic knowledge, especially when AI handles routine coding tasks—focus on real-world scope and decision-making ability.
- **Capture the value created by AI productivity gains** by clearly defining who benefits from the 10x boost that tools like Claude Code provide to engineers, and ensure your compensation and equity structures reflect this shift.
- **Implement prompt injection defense strategies** for AI agents in production, treating social engineering attacks on agents with the same rigor as you would attacks on human employees.
- **Monitor hiring and cultural shifts** as companies adapt to AI-driven development—use hiring practices as a leading indicator of how organizations are evolving their technical strategy and values.

**27.** [Your manager is already investing in you](https://newsletter.weskao.com/p/your-manager-is-already-investing) — *Wes Kao* · Mar 04, 2026

Your manager is already investing in you through feedback and coaching, but you may not recognize it because you're romanticizing what mentorship should look like. The key to getting more coaching is to make it easy for your manager by asking specific, actionable questions about recent work rather than vague requests for growth.

- **Reframe feedback as investment**: Recognize that detailed, critical feedback from your manager is actual coaching and mentorship, not a sign they don't believe in you.
- **Make feedback worth your manager's time**: Frame requests around how addressing them will save money, make money, or add value to the business, since senior leaders prioritize firm value.
- **Ask specific, real-time questions**: Instead of vague asks like "How do I get to the next level?", ask targeted questions about recent work like "What could I have done differently in that presentation?" to minimize cognitive load.
- **Become worth investing in**: Display strong judgment, continuous improvement, and openness to direct feedback so your manager feels motivated to coach you rather than avoiding it.
- **Draw out insights with targeted prompts**: Use specific questions like "What would you do differently?", "What grade would you give this?", or "What risks did I miss?" to actively invite your manager's coaching.

**28.** [Get Started with Claude Code + Cowork Today](https://www.news.aakashg.com/p/claude-cowork-code-setup) — *Product Growth* · Mar 04, 2026

Claude Code and Claude Cowork represent transformative new professional software tools, but the primary challenge users face is getting started with them effectively.

- **Adopt Claude Code and Cowork** to unlock significant productivity gains, as these tools are among the most important professional software innovations in recent years
- **Overcome implementation barriers** by following a structured getting started guide designed to help users quickly realize value from these platforms
- **Prioritize mastery of these tools** to position yourself among the most productive professionals, as they represent a fundamental shift in how work can be accomplished

**29.** [How to debug a team that isn’t working: the Waterline Model](https://www.lennysnewsletter.com/p/how-to-debug-a-team-that-isnt-working-d43) — *Lenny's Newsletter* · Mar 03, 2026

Molly Graham presents the Waterline Model, a diagnostic framework that helps managers identify the true root causes of team underperformance by examining structural and environmental factors before blaming individuals.

- **Avoid the blame trap** by recognizing that jumping to personnel changes is often the wrong first step when diagnosing team problems.
- **Use the Waterline Model layers** systematically to diagnose issues in order, starting with structural factors before examining individual performance.
- **Snorkel before you scuba** by conducting shallow investigations first to understand the full context before making deep organizational or personnel decisions.
- **Recognize rational behavior** in faulty environments—poor performance may reflect reasonable adaptation to broken systems rather than individual capability issues.

