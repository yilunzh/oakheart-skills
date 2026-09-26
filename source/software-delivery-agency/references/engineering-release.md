# Engineering and release

Read the actual project and instructions; use Sites for Sites projects. Preserve the chosen replacement/integration boundary. A checkout design is not a booking replacement until inventory, payment states, records, notifications and staff operations work.

Reuse program/car, availability, configuration, inquiry, checkout and staff-queue components. Document system of record and interfaces. Model holds/expiry, payment pending/success/failure, confirmation, cancellation/refunds and resource conflicts. Prevent overselling transactionally and handle duplicate webhooks idempotently. Reconcile uncertain outcomes before retrying.

For internal tools model roles, access, audit and recovery. Test tenant/role boundaries. Keep secrets server-side and collect only needed personal data.

## Acceptance

Inspect the actual candidate version; capture artifact, date, version and result. Independent QA gets the artifact without a desired score. Disclose unavailable independent execution.

| Surface | Required consequential evidence |
| --- | --- |
| All | Mobile/desktop completion, keyboard/errors, approved claims, comparable performance, ownership/rollback |
| Leads | Destination receipt, deduplication, invalid/error behavior and staff routing |
| Booking | Availability conflict, hold expiry, payment success/failure, duplicate webhook, confirmation, cancellation/refund, staff reconciliation |
| Internal tool | Authentication, role/tenant boundaries, staff task completion, audit and restore |
| Migration | Redirect map, metadata/canonical/indexability, inbound paths and recovery |

Use consistent Lighthouse settings and repeated comparable runs; distinguish lab/field evidence. Preserve useful search content/URLs. An inaccessible system cannot receive a fabricated pass.

Fix consequential blockers and retest affected journeys. Run `agency_checks.py check <record> --stage release` for evidence completeness, then inspect the evidence. It does not execute tests, verify claims or grant release permission.

Release within actual authorization and Hosting instructions. Verify public behavior afterward, record deployment ID and execute approved rollback when needed. Confirm actual support owner and response commitments.
