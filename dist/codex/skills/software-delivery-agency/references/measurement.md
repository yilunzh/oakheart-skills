# Measurement and guarantee

Read actual analytics and booking/CRM evidence or mark missing access/data. Reconcile definitions, periods, channel mix, bots/internal traffic, repeat visitors, offline closes, cross-domain booking and tracking loss. Missing baseline does not block design; it blocks established guarantee eligibility.

Agree before testing on primary outcome, eligible population/randomization unit, qualification rules, attribution window, baseline, meaningful effect, sample/power assumptions, duration, decision rule, guardrails, exclusions and treatment of invalid/inconclusive results. Keep the full agreement in the dossier; a boolean is insufficient.

Covered website agency fees are not earned without the agreed demonstrated improvement. Disclose third-party costs beside the offer. Do not introduce an upfront agency fee contradicting the promise. Fix handoff/ownership and support terms. These are commercial design requirements, not a jurisdiction-specific contract.

## Instrument and plan

Prefer concurrent randomization with stable user assignment when feasible. Track qualifying outcomes, not clicks or confirmation views alone. Separate inquiry, qualification and booking; deduplicate paid bookings by transaction ID and reconcile refunds. Verify attribution across booking domains. Permissible exports can supply evidence when connectors cannot; label freshness.

Account for repeat users, consent missingness and channel mix. Check assignment balance and event loss/duplication. Pre/post comparisons are observational. Do not switch outcomes, cherry-pick periods or repeatedly peek at fixed-horizon significance. Prespecify a fixed horizon or appropriate sequential method.

Run `python scripts/agency_checks.py sample-size --baseline 0.02 --target 0.03 --monthly-visitors 1000` for an approximate equal-allocation, two-proportion fixed-horizon design. Defaults: two-sided alpha .05, power .80, independent visitors and binary outcomes. Cluster designs, rare events or sequential methods need appropriate alternatives. Traffic means visitors eligible for the experiment, not total sessions.

If the sample cannot accrue in the agreed window, eligibility is unqualified or unresolved. Consider a longer bounded period or a separately scoped alternative if the buyer chooses it. A hypothesized larger effect is not achieved uplift. Never manufacture traffic or guarantee terms.

## Decide

Report counts/denominators, absolute percentage-point and relative differences, interval/uncertainty, design, dates and guardrails. Apply the precise prespecified threshold: a positive difference need not meet an agreement promising a minimum effect. Outcomes: win, loss, inconclusive, invalid. Inconclusive/invalid is not a paid win. Stop/extend only as agreed, without unlimited unpaid optimization.

Guardrails may include lead quality, booking value, cancellations/refunds, capacity and contribution. Internal tools may instead target response time, errors, completion or quote-to-sale conversion. Do not force website conversion guarantees onto operational tools.
