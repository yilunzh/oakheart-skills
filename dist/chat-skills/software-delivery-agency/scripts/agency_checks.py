"""Offline planning and evidence completeness. Never executes external actions."""
import argparse
import json
import math
from statistics import NormalDist


STAGES = {
    "qualify": ["buyer_fit", "capacity", "baseline", "measurement_agreement"],
    "research": ["buyer_brief", "offer_facts", "incumbent_audit"],
    "design": ["scope", "journey", "content", "measurement_spec"],
    "build": ["implementation", "functional_tests"],
    "release": ["journey_tests", "accessibility", "claims", "performance", "rollback"],
    "measure": ["measurement_agreement", "assignment_integrity", "outcome_reconciliation", "decision_analysis", "guardrails"],
}
SURFACES = {
    "lead": ["lead_delivery", "lead_errors"],
    "booking": ["availability_conflict", "hold_expiry", "payment_states", "webhook_dedup", "confirmation_delivery", "refund_flow", "staff_reconciliation"],
    "internal": ["authentication", "role_boundaries", "staff_task", "audit_restore"],
    "migration": ["redirects", "indexability"],
}


def sample_size(baseline, target, monthly_visitors=None, alpha=.05, power=.8):
    vals = (baseline, target, alpha, power)
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in vals):
        raise ValueError("Rates, alpha and power must be finite numbers.")
    if not 0 < baseline < target < 1:
        raise ValueError("Require 0 < baseline < target < 1; rates are proportions.")
    if not 0 < alpha < 1 or not .5 < power < 1:
        raise ValueError("Require 0 < alpha < 1 and .5 < power < 1.")
    if monthly_visitors is not None and (isinstance(monthly_visitors, bool) or not math.isfinite(monthly_visitors) or monthly_visitors <= 0):
        raise ValueError("Monthly eligible visitors must be positive and finite.")
    p = (baseline + target) / 2
    z = NormalDist().inv_cdf(1-alpha/2)
    zp = NormalDist().inv_cdf(power)
    n = math.ceil((z*math.sqrt(2*p*(1-p)) + zp*math.sqrt(baseline*(1-baseline)+target*(1-target)))**2 / (target-baseline)**2)
    return {"per_variant": n, "total_visitors": 2*n,
            "estimated_months": round(2*n/monthly_visitors, 2) if monthly_visitors else None,
            "absolute_percentage_points": round(100*(target-baseline), 4),
            "relative_lift_percent": round(100*(target/baseline-1), 4),
            "alpha_two_sided": alpha, "power": power,
            "method": "Normal approximation, equal allocation, independent visitors, binary outcomes, fixed horizon",
            "limitation": "Planning estimate, not evidence of uplift or guarantee eligibility."}


def check(record, stage):
    if stage not in STAGES:
        raise ValueError("Unknown stage")
    if not isinstance(record, dict) or record.get("schema_version") != 1:
        raise ValueError("Expected client record schema_version 1")
    surfaces = record.get("surfaces", [])
    if not isinstance(surfaces, list) or any(x not in SURFACES for x in surfaces):
        raise ValueError("Surfaces must be a list drawn from lead, booking, internal, migration")
    evidence = record.get("evidence", {})
    if not isinstance(evidence, dict):
        raise ValueError("Evidence must be an object")
    requirements = list(STAGES[stage])
    if stage == "release":
        for surface in set(surfaces):
            requirements.extend(SURFACES[surface])
    missing = []
    issues = []
    if stage in ("build", "release") and not record.get("release_id"):
        issues.append("A candidate release_id is required.")
    if stage == "release" and not surfaces:
        issues.append("Declare applicable surfaces before release review.")
    for requirement in requirements:
        e = evidence.get(requirement)
        if not isinstance(e, dict) or e.get("status") != "verified" or not all(isinstance(e.get(k), str) and e[k].strip() for k in ("artifact", "observed_at", "reviewer")):
            missing.append(requirement)
        elif stage in ("build", "release") and e.get("release_id") != record.get("release_id"):
            missing.append(requirement + ": stale candidate version")
    return {"stage": stage, "evidence_complete": not missing and not issues,
            "missing": missing, "issues": issues,
            "decision_scope": "Completeness only. Inspect evidence, applicable scope and actual authorization. This is not a release, payment or eligibility decision."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    s = sub.add_parser("sample-size")
    s.add_argument("--baseline", required=True, type=float)
    s.add_argument("--target", required=True, type=float)
    s.add_argument("--monthly-visitors", type=float)
    s.add_argument("--alpha", type=float, default=.05)
    s.add_argument("--power", type=float, default=.8)
    c = sub.add_parser("check")
    c.add_argument("record")
    c.add_argument("--stage", choices=STAGES, required=True)
    args = parser.parse_args()
    try:
        if args.command == "sample-size":
            result = sample_size(args.baseline, args.target, args.monthly_visitors, args.alpha, args.power)
        else:
            with open(args.record, encoding="utf-8") as f:
                result = check(json.load(f), args.stage)
        print(json.dumps(result, indent=2, allow_nan=False))
        if args.command == "check" and not result["evidence_complete"]:
            raise SystemExit(2)
    except (ValueError, OSError, TypeError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
