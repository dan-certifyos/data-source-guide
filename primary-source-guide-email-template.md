# Primary Source Reference Guide — Email Template

A generic follow-up email for sharing the **Primary Source Reference Guide**
(`certifyos-primary-source-reference.pdf`) with a client. It highlights the
guide's contents and its built-in navigation.

> **Send the PDF as an attachment.** The internal/GCS URL for the guide requires
> a `@certifyos.com` login, so it won't work for clients — attach the PDF
> instead. The live navigation (clickable category bar and "see index"
> jump-links) lives inside the document; email clients can't link into a PDF
> attachment's sections, so the email describes that in-document navigation.

Replace the `{{PLACEHOLDERS}}` before sending.

---

**Subject:** CertifyOS Primary Source Reference Guide — where your monitoring data comes from

Hi {{CLIENT_TEAM}},

Following up on this month's reports, I wanted to share a reference that explains *where* all of the underlying data comes from. I've attached our **Primary Source Reference Guide** (`certifyos-primary-source-reference.pdf`).

For every credential and sanction we monitor, the guide identifies the authoritative issuing body we pull from directly — not a secondary aggregator or data vendor — along with the source name, custodian/authority, source URL, access method, and refresh cadence. It's the "source of truth" behind the flags and summary files in your reports.

**What's inside**

The first part is an overview, organized by category:

- **Provider Identity** — NPI (NPPES Registry / CMS) and deceased verification (SSA Death Master File)
- **Licensure** — state professional licenses (all 50 states + DC), DEA registration, and state CDS / controlled-substance licenses
- **Board Certification** — ABMS board certification for MD/DO providers
- **Sanctions & Exclusions** — NPDB adverse actions, OIG LEIE, state Medicaid exclusion lists, SAM.gov, OFAC SDN, and state board licensure actions
- **Medicare Participation Status** — Medicare Opt-Out affidavits (CMS)
- **Provider Attestation** — CAQH ProView (application, disclosure questions, hospital affiliations, malpractice coverage)

The second part contains detailed, per-state source indexes for the areas that span many boards:

- **State Licensing Authority Index** — sources across all 50 states + DC
- **CDS State Source Index** — the jurisdictions that require a separate state controlled-substance registration
- **State Medicaid Exclusion Source Index** — jurisdictions with direct list URLs
- **Board Licensure Action Source Index** — state board portals

**How to navigate it**

The PDF is built to jump around quickly:

- The **category bar** at the top of the document is clickable — select any category (Provider Identity, Licensure, Board Certification, Sanctions & Exclusions, Provider Attestation) to jump straight to that section.
- Where a row covers many boards, look for the **"see index"** link — it jumps down to the matching per-state index table further in the document.

This pairs directly with the reports you receive: the credential types we flag (State, DEA, CDS, Board, sanctions/exclusions, Medicare Opt-Out) each map to a section in this guide.

Please don't hesitate to reach out if you have any questions about a particular source or how we refresh it.

Best,
{{YOUR_NAME}}
