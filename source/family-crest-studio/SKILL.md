---
name: family-crest-studio
description: Create and refine personal family crests, coats of arms, monograms, and heirloom emblems. Use for discovering family symbolism, exploring broad style directions, writing multilingual mottos, preserving a selected design, coordinating independent quality review, or preparing crest artwork for an engraving vendor. Ask targeted questions when meaningful information is missing; never turn production cleanup into an unrequested redesign.
metadata:
  version: "0.2.1"
  status: "candidate"
---

# Family Crest Studio

Create a meaningful family emblem, then preserve it faithfully through refinement and physical-production preparation. Follow the host's tool, safety, and approval rules. This skill does not grant tools, spending permission, or automatic installation.

## 1. Route the request

Choose the current mode; do not restart completed stages:
- **Discover:** establish the personal brief and intended use.
- **Style panorama:** show a wide range of stylistic directions and help the user narrow preferences.
- **Explore:** generate a smaller set of serious directions inside the chosen style lane.
- **Refine:** change only the aspects the user requests.
- **Judge:** obtain an independent quality review when available, otherwise label the review as self-review only.
- **Prepare:** adapt the approved artwork for vendor review, without redesigning it.

Recover relevant conversation facts and the exact available source image first. Resolve “the second one” against its particular round. If the source is missing or genuinely ambiguous, ask for that image or selection; never reconstruct it from memory. A thumbnail, filename, or remembered description is not a production master.

## 2. Ask only what changes the next decision

Use known answers. Ask **at most four grouped questions per round**, prioritizing unresolved identity, symbolism, style, intended use, and fabrication constraints. Do not overwhelm the user with fabrication terminology.

Before a personal concept, establish the displayed name/script, who or what is represented, meaningful values or experiences, and aesthetic direction. Offer examples when the user is unsure. Distinguish unknown facts from creative choices the user has delegated. Never invent ancestry, relationships, dates, national identity, mottos, or animal-to-person mappings as facts.

Before exact production preparation, resolve the selected master, permitted changes, intended physical dimensions, and material/process constraints. Unknown vendor capabilities may remain an explicit blocker; they need not stop a quote package. Ask budget, destination, and deadline only when needed for sourcing or commissioning. See [Discovery](references/discovery.md).

Record decisions and open questions in [Project state](assets/project-state.template.json). Keep personal information in the project, not in this reusable skill.

## 3. Start broad on style, then converge

When the user has not already locked a style, begin with a **style panorama**. Default to **4–6 genuinely distinct directions** with short labels and a one-line explanation each. Vary form language, density, mood, and cultural treatment—not just color.

Good style panorama categories include combinations like:
- European imperial / ornate heraldic
- Vintage engraving / black-and-white etching
- Eastern ink / literati seal style
- Modern minimalist monogram
- Luxury emblem / fashion-house style
- Storybook or fine-art illustration

If images are allowed, generate the styles visually. If not, describe them clearly first. After presenting the panorama, explicitly ask the user to narrow to one or two preferred lanes before deeper refinement. If the user gives mixed signals, summarize their apparent preference and ask for confirmation rather than guessing.

During the narrower **Explore** mode, default to three serious directions within the chosen lane, labeled with stable IDs. Explain the difference briefly before generating, where the host permits. Do not equate a new color palette with a new design. Develop three to five short motto pairs when copy is the open decision; favor meaning, warmth, rhythm, and specificity over generic grandeur. Separate literal translation from a complementary bilingual motto. Verify spelling, script, and meaning; do not silently switch simplified/traditional characters.

Use culturally informed typography, not caricature. Treat modern commissioned heraldry as personal artwork, not evidence of inherited arms or rank. Use the host's image tools for visual creation; text-only recommendations do not fulfill an image request.

## 4. Lock approval; constrain edits

On explicit selection, record the reference ID, accessible source path, version, and SHA-256 when available. Lock layout, aspect ratio, motif placement, animal appearances, lettering, exact copy, and decorative structure. Do not treat silence as approval.

**Change only the requested dimension.** Copy exploration is not permission to replace imagery; engraving cleanup is not permission to rewrite a slogan, change a face, add a crown, move a pet, swap a national symbol, or redesign a font. Record each permitted exception. A newly proposed exception requires approval before promotion to the master.

Work from the locked source, not from a new description. Prefer source-preserving processing when the host permits. When image editing tools are required, anchor the supplied original and reject outputs that drift. Never label a regenerated approximation “the same design.” If faithful editing cannot be achieved, provide the reference and a vendor correction brief instead of claiming cleanup succeeded.

## 5. Require independent judging when possible

See [Review](references/review.md). Separate creator work from judging work. The creator must not grade its own output as independent review.

When the runtime supports a genuinely separate execution, use an **independent judge pass** after exploration, after major refinement, and before vendor delivery. The judge should receive: the user brief, the locked master when one exists, permitted changes, the candidate output, and stage-appropriate criteria. The judge should **not** receive the creator's self-rating or preferred answer.

Judge output should cover:
- brief fidelity and symbolism accuracy
- visual quality and coherence
- typography and copy quality
- preservation of locked elements
- production-claim accuracy
- explicit pass / revise / reject decision

If the runtime does **not** support separate execution, label the result **self-review only** and say independent judging is unavailable in the current environment. Do not imply independence with role-play, hidden chain-of-thought, or “another internal agent” in the same context.

Automatic rejection conditions include: wrong selected source, unauthorized layout changes, wrong wording, spelling/script errors, omitted required motifs, or unverified production claims.

## 6. Prepare for the actual fabrication process

Read [Production](references/production.md) only in this mode. Inspect actual files. Separate aesthetic approval from production readiness. Remove simulated paper/background effects only as appropriate to the chosen process; retain the original unchanged.

Measure output scale and examine the finest strokes, gaps, faces, and smallest lettering. Do not invent universal engraving limits. Request the fabricator's specifications. Upsampling or changing DPI metadata does not establish additional source detail; automatic tracing is not a manual redraw. SVG/PDF extensions alone do not prove vector artwork.

Use [the read-only inspector](scripts/inspect_artwork.py) for hashes, raster dimensions, placed-size PPI, or SVG structure. For raster placed-size PPI, pass `--width-inches` and/or `--height-inches`; one dimension assumes the original aspect ratio, while two report each axis and whether the aspect ratio is preserved. Without physical dimensions, PPI is not calculated. It does not certify fidelity or engravability.

## 7. Review and deliver

Compare original and derivative at the same scale, including text and face crops. Check spelling, unchanged anchors, clipping, file integrity, and the actual deliverables. Fix or disclose failures; do not hide them behind a score.

For a vendor handoff, include the original reference, cleaned derivative when actually produced, comparison proof, exact-text record, specifications/open questions, and a brief based on [this template](assets/vendor-brief.template.md). Provide only formats actually created and verified. Record source/version and transformations. Propose a final-scale physical detail sample before production authorization.

Label status precisely: **concept**, **style panorama**, **selected design**, **refined design**, **self-reviewed only**, **independently reviewed**, **prepared for vendor review**, or **vendor-validated for a stated process and size**. State what changed, what stayed fixed, and what remains unverified.

For skill changes, use [behavioral scenarios](evals/scenarios.json). Passing helper tests is not proof of better model behavior.
