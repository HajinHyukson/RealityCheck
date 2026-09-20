# RealityCheck dashboard studio

## Combined workspace

Open `http://127.0.0.1:8035/workspace.html` for the completed constellation + package-history option. It defaults to FluxRail and combines the branching original/adopted/proposed history diagram with the evidence network and a shared selection inspector. History markers focus the map; covenant records use the package version at the selected review. Package comparison preserves before/after text and pending proposals. `verify-workspace.cjs` checks these behaviors without any backend writes.

Five complete, independent frontend alternatives use one snapshot of actual project records:

- `constellation.html`: source / assumption / provision network with pan, zoom, review focus, library and register.
- `board.html`: report queue, investigation branches, evidence and recorded findings.
- `desk.html`: document library, full source reader and connected evidence.
- `storyline.html`: dated reports, assessment history and contractual versions.
- `matrix.html`: document-to-assumption relationships and evidence coverage.

## Run

```powershell
python -m http.server 8035 --bind 127.0.0.1 --directory dashboard-studio
```

Open `http://127.0.0.1:8035/`. This folder is a static site; it can be hosted by any static web server. No build step, external library or backend connection is required. Serve this folder only, not the repository root.

The design picker navigates between full independent pages while retaining company and selected review. Company switching, search, evidence dialogs, source downloads and JSON snapshot export work locally. Review notes are saved in browser localStorage and never written to lender or benchmark records.

## Data

The default case is iRobot; RumbleOn and fictional FluxRail are also available. Read `DATA.md` for exact provenance, source boundaries and reviewer corrections. Rebuild the snapshot without model calls:

```powershell
python dashboard-studio/build_data.py
```

These frontends show saved analyses. Inference, ingestion, user authentication, shared note storage, and contractual approvals are not connected. Nothing in these screens modifies the operative agreement or publishes a model result. Public-company histories remain dated historical snapshots. FluxRail is clearly marked synthetic.

## Verification

`verify.cjs` uses Playwright to exercise the five dashboards against the local server: company switching, real-source inspection, search, design navigation, and responsive overflow checks. Point `NODE_PATH` at the installed Playwright package directory and run `node dashboard-studio/verify.cjs`.
