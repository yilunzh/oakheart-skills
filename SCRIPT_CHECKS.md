# Local verification — 2026-09-26

- Source preservation: 55 files matched recorded SHA-256 hashes.
- Package structure: 12 generated skill folders, 6 individual chat ZIPs, and 2 JSON plugin manifests passed local checks.
- Relative Markdown references: 78 checked, no missing files.
- Learning-loop checker: 26 existing unit tests passed on the generated Code package.
- Agency checker: 8 existing unit tests passed on the generated Code package.
- Crest inspector: successfully inspected the bundled SVG icon; reported SVG structure and actual file hash. This is a helper smoke test, not visual validation of a crest.
- No Claude CLI is installed here. Claude import, native plugin validation, automatic invocation, connector access, and behavioral parity have not been tested.
- No PTC, AutoNation, or Oakheart task comparisons were run during this export.

These checks establish file preservation and limited local executable compatibility. They do not demonstrate improved or equivalent model behavior.

Independent static review inspected source preservation, generated packages, dependencies, and installation instructions. It found no blocker in the generated Linux packages. Findings about source inventory checks, manifest counts, optional reviewer namespace, portable path formatting, full adaptation diffs, archive fidelity, and failed-rebuild preservation were addressed. A deliberate source-inventory failure confirmed that the previous distribution remains intact. Windows rebuilds have not been executed on Windows.

Follow-up independent static review verified all four final fixes on current bytes with no remaining findings in that scope. It did not rerun failure injection or execute Claude.
