Vireo Audio — Support Ticket Routing & Headcount Note
To: Priya Raman, Head of Customer Experience
Subject: What the support export says about Billing headcount

Bottom line
Billing is the largest first-routed team in the Jan 2025–Jun 2026 window: 2,425 of 11,641 tickets (20.8%). That confirms the broad direction of your note, but the data also shows a process problem worth addressing before treating queue volume as the sole hiring signal.

What I found
• Billing's first-response breach rate is 19.7%, versus 11.1% across the desk. At Rs 350 per breach, the Billing queue is carrying a material SLA-credit cost.
• Billing recorded 632 team hand-offs in the window. The policy values each internal transfer at Rs 305, so those recorded transfers represent Rs 192,760 of transfer cost before considering the underlying customer impact.
• The category tag is not reliable enough to use blindly. A text model trained on the historical tags agrees with the existing tag on 83.9% of a stratified 20% holdout (2,329 tickets), leaving a 16.1% disagreement rate. This is an agreement measure, not ground-truth accuracy, because the historical tags are the labels being questioned.
• The model surfaces 430 tickets (3.7%) where the inferred issue category implies a different owning team than the first-routed team. These are review candidates, not automatically “wrong” tickets.

A measurable operating goal
Reduce Billing's first-response breach rate from 19.7% to 12% over the next quarter. At roughly 650 tickets/week and the current mix, that corresponds to about Rs 189,000/year of avoided SLA-credit cost if sustained. This is a process target, not a guaranteed saving.

Recommendation for the next step
Keep the two-hire decision visible, but do not use raw category volume as the only trigger. Use the classifier to identify likely misroutes and low-confidence tickets, tighten Billing intake rules, and review Billing's breach/transfer rate weekly for four weeks. If volume remains high after routing is cleaned up, the headcount case will be cleaner.

Scope and caveats
The export contains a small number of pre-2025 legacy rows even though the brief says Jan 2025–Jun 2026; those rows were excluded from the headline analysis. Legacy resolution timestamps also require the policy's UTC/IST reconciliation before handle-time analysis. I did not use Tier 2 volume as a hiring comparison because the policy explicitly says Tier 2 work is multi-touch and should not be compared with Tier 1 on weekly ticket volume.

The tool is deliberately conservative: it shows the suggested category and confidence, and sends low-confidence cases to review rather than silently auto-routing them.
