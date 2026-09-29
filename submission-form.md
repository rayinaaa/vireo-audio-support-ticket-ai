# Vireo Audio — Submission Form

**What did you build, and what business outcome does it move? State the number and the money.**

Built a Streamlit AI-assisted support-ticket categorisation and routing-audit tool. It combines word/character TF-IDF features with logistic regression, shows category and team volumes by month, and surfaces low-confidence and potential routing-mismatch tickets.

Business goal: reduce Billing's first-response breach rate from **19.7% to 12%**. At ~650 tickets/week and the current mix, that is approximately **Rs 189,000/year** of avoided Rs 350 SLA-credit cost if sustained. The analysis window contains 11,641 tickets; Billing is 2,425 tickets / 20.8%.

**What does one run cost, and what would a month cost at Vireo's volume (roughly 650 tickets a week)? Show the arithmetic. If you used no paid calls, say so.**

**Rs 0 in paid API/model calls.** The submitted tool runs locally with scikit-learn.

Monthly volume assumption: 650 × 52 / 12 ≈ **2,817 tickets/month**. Since inference is local CPU, incremental model/API spend is **Rs 0/run** and **Rs 0/month**. This excludes the user's own machine/cloud electricity/hosting cost.

**How do you know it works? Sample size, how you checked, error rate, and the kind of case it gets wrong.**

I used a stratified 80/20 holdout: **9,312 train / 2,329 test tickets**. The model agrees with the historical category tag on **83.9%** of the holdout; disagreement/error rate against that historical label is **16.1%**.

Important limitation: this is not a ground-truth accuracy score because the historical tags are exactly what the task says may be poor. The tool therefore also emits a **200-ticket review queue** and treats low-confidence predictions (<60%) as human-review candidates.

Typical difficult cases: mixed-intent messages such as delivery + refund, cancellation + payment, and technical complaints where the closing note contains a later escalation. “Other” is the noisiest historical class.

**Did you change, narrow, or push back on the client's ask? What, when, and why.**

Yes. I kept the requested monthly category/team chart, but I did not treat “largest team gets two hires” as a sufficient causal conclusion. The policy says Tier 2 should not be compared with Tier 1 on volume, so I excluded Tier 2 from that comparison. I also used the stated Jan 2025–Jun 2026 window rather than silently including legacy rows outside it.

I reframed the actionable business outcome around Billing's first-response breaches and transfers, because Finance explicitly asked whether a process fix could be preferable to hiring.

**What is wrong with what you are handing us? Be specific.**

1. The classifier learns from historical tags, so its 83.9% holdout score measures agreement with the existing tagging process, not truth.
2. The historical “Other” class is noisy; some cases are obvious delivery, billing, warranty or product-enquiry cases.
3. The routing mismatch signal is a review queue, not proof of misrouting.
4. Legacy handle-time data requires the UTC/IST reconciliation described in the policy; I did not use raw legacy timestamps for headline handle-time conclusions.
5. The app retrains on startup; there is no persisted model registry/versioning.
6. The current prototype has no authentication, database, production monitoring or feedback loop.
7. The submission pack does not include a completed public GitHub/Drive link or screen recording because those external destinations were not available from this environment.

**What did you deliberately leave out, and why that rather than something else?**

I left out a production-grade LLM/API integration, live helpdesk integration, customer-level forecasting, detailed staffing simulation, and automated ticket reassignment. Those would consume the time budget without improving the first decision enough. I prioritised a runnable classifier, validation, monthly breakdown, routing review queue, and quantified business case.

I also did not compare Tier 2 with Tier 1 on volume because the policy explicitly says not to.

**Anything you built or found that nobody asked for?**

Yes: a routing-mismatch review queue, confidence-based human review, and a data-quality check for the legacy timestamp issue. The tool also lets an operator paste a new ticket and receive a category + confidence score.

**What did you use AI for? Which tools and models, where they helped, where they wasted your time, what you threw away. Link your three-minute screen recording here.**

Used ChatGPT/GPT-5.6 Luna for analysis planning, code generation/debugging, interpretation of the brief, and drafting the memo/submission wording. The actual categorisation model in the submitted app is local scikit-learn TF-IDF + logistic regression; no paid LLM inference is required.

AI was useful for quickly exploring alternative validation approaches and turning the business findings into a concise memo. I discarded attempts to make a fully LLM-dependent classifier because it would add API cost, credentials, latency and non-determinism without solving the weak-label problem.

Screen recording: **[ADD PUBLIC GOOGLE DRIVE RECORDING LINK]**

**Your Public Google Drive Link**

**[ADD PUBLIC GOOGLE DRIVE FOLDER LINK]**

**Someone picks this up on Monday and you are unreachable. The three things they need to know.**

1. Run `pip install -r requirements.txt` and then `streamlit run app.py`.
2. The headline analysis is Jan 2025–Jun 2026; legacy rows outside that window are excluded.
3. Treat AI predictions and routing mismatches as review signals, not automatic truth. The historical labels are noisy.

**Honest hours spent.**

**5**

**Github Repo Link**

**[ADD PUBLIC GITHUB REPO URL]**
