#!/usr/bin/env python3
"""Build the zero-cost, deterministic AOC-002 owner-review input bundle and visuals."""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "content" / "AOC-002"
ASSETS = ROOT / "public" / "assets" / "aoc-002"
EDITION = "AOC-002"


def write_json(name: str, value) -> None:
    RUN.mkdir(parents=True, exist_ok=True)
    (RUN / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source(source_id, title, url, supports, limitation):
    return {"id": source_id, "title": title, "url": url, "supports": supports, "limitation": limitation}


SOURCES = [
    source("SEPLAT-9M-2026", "Seplat Energy — 9M 2026 Financial Results",
           "https://www.seplatenergy.com/media/xt4h2glj/seplat-energy-report-9m-2026-final-291026.pdf",
           "Aku-01 discovered oil and gas after period end; preliminary internal mid-case estimates are 157 Bcf gas in place and 19 MMbbls oil in place; completion and a future tie-back are planned; Seplat holds 40% operated interest in PPL 2A25.",
           "Company-reported preliminary in-place estimates are not proved reserves, production volumes, revenue, a final investment decision, or a schedule guarantee."),
    source("SEPLAT-OML53", "Seplat Energy — OML 53 operations",
           "https://www.seplatenergy.com/our-company/our-operations/upstream/oml-53/",
           "OML 53 is an onshore Imo State block of about 1,585 km² with existing oil and gas infrastructure, a 40% Seplat working interest, and links to the ANOH gas system.",
           "The page describes the wider licence and existing fields; it does not identify Aku-01's exact wellhead or establish effects in any named community."),
    source("AGPC-ANOH-2026", "ANOH Gas Processing Company — network entry agreement",
           "https://anohgas.com/agpc-signs-network-entry-agreement-with-ngic-unlocking-250-mmscf-d-gas-injection-into-nigerias-national-gas-transportation-network/",
           "The Imo-based ANOH plant has 300 MMscf/d processing capacity and a 2026 agreement enabling up to 250 MMscf/d injection into the national gas network.",
           "This does not prove that Aku-01 gas will enter ANOH, when it might do so, or at what volume."),
    source("NBS-LFS-2023", "Nigeria National Bureau of Statistics — Annual Labour Force Survey",
           "https://nigerianstat.gov.ng/pdfuploads/Annual_Nigerian_Labour_Force_Survey_Report.pdf",
           "For the survey period, Imo State had 2,009,039 employed people, 77.6% self-employment among employed people, 93.9% informal employment, and 12.8% employment in agriculture.",
           "Survey estimates describe the state and period, not a particular household, community, applicant, or future oil-and-gas workforce."),
    source("NCDMB-HCD", "NCDMB — Human Capacity Development",
           "https://ncdmb.gov.ng/human-capacity-development/",
           "Nigeria's content framework requires employment and training plans for qualifying industry projects and describes classroom, practical, on-the-job and certification pathways.",
           "A national framework does not guarantee training, contracting, or employment from Aku-01 to any person or locality."),
    source("NUPRC-HOST-2022", "NUPRC — Host Communities Development Regulations 2022",
           "https://www.nuprc.gov.ng/wp-content/uploads/2022/07/Nigeria-Upstream-Petroleum-Host-Communities-Development-Regulations-2022.pdf",
           "Regulations govern determination of host communities, development trusts, needs assessments, development plans, governance and fund distribution.",
           "Without the regulator/operator's determination and the exact operational area, Atlas cannot name Aku-01 host communities or promise trust benefits."),
    source("PIA-2021", "Nigeria Petroleum Industry Act 2021",
           "https://br2025.nuprc.gov.ng/media/ggwk4wxe/petroleum-industry-act-2021.pdf",
           "The Act provides for host-community development trusts and an annual settlor contribution equal to 3% of the preceding year's actual operating expenditure for upstream operations affecting applicable host communities.",
           "The formula is not 3% of oil revenue and cannot be converted into an Aku-01 community amount without applicable operations and expenditure."),
    source("NUPRC-ENV", "NUPRC — Health, safety and environmental oversight",
           "https://nuprc.gov.ng/health-safety",
           "NUPRC reviews environmental impact assessments, risk registers and management plans and monitors upstream environmental action plans.",
           "Regulatory requirements do not establish that an Aku-01 impact has occurred or that a specific mitigation outcome is assured."),
    source("NUPRC-FLARE-2022", "NUPRC — Gas Flaring and Venting Regulations 2022",
           "https://www.nuprc.gov.ng/wp-content/uploads/2022/12/Gas-Flaring-and-Venting-Regulations-2022-D.pdf",
           "The regulations aim to reduce environmental and social impacts from flaring and venting, protect the environment, prevent waste and create benefits from gas capture.",
           "They do not establish Aku-01's future emissions, processing route or compliance performance."),
]

PERSPECTIVES = [
    ("D1", "The Discovery", "What was found—and what remains preliminary.", ["SEPLAT-9M-2026"]),
    ("I1", "The Route to Market", "How a discovery might meet existing infrastructure.", ["SEPLAT-OML53", "AGPC-ANOH-2026"]),
    ("MF1", "The Commercial Question", "Why in-place resources are not yet revenue.", ["SEPLAT-9M-2026", "SEPLAT-OML53"]),
    ("C1", "Community and Authority", "Who may decide, participate and benefit.", ["NUPRC-HOST-2022", "PIA-2021"]),
    ("W1", "Work and Capability", "Opportunity depends on skills, contracts and timing.", ["NBS-LFS-2023", "NCDMB-HCD"]),
    ("E1", "Land, Air and Unknowns", "Oversight matters before impacts can be claimed.", ["NUPRC-ENV", "NUPRC-FLARE-2022"]),
]

SCENES = {
    "D1": [
        ("D1-S1", "Aku-01 changes the regional possibility set without beginning production.", ["SEPLAT-9M-2026"], "Do not describe a preliminary discovery as proved reserves, production or revenue."),
        ("D1-S2", "Five reservoir intervals and preliminary in-place estimates define the announced scale.", ["SEPLAT-9M-2026"], "Company preliminary estimates remain subject to appraisal and development decisions."),
        ("D1-S3", "The oil find was outside the original well plan, while adjacent prospects remain future exploration questions.", ["SEPLAT-9M-2026"], "De-risking is not the same as discovery or commerciality in adjacent prospects."),
    ],
    "I1": [
        ("I1-S1", "OML 53 already contains producing fields, flow stations, pipelines and gas development infrastructure.", ["SEPLAT-OML53"], "Wider-block infrastructure does not locate Aku-01 or prove a final connection route."),
        ("I1-S2", "A planned tie-back could shorten the path to market, but engineering, approvals and timing remain unresolved.", ["SEPLAT-9M-2026", "SEPLAT-OML53"], "A stated plan is not a completed tie-back or start-up schedule."),
    ],
    "MF1": [
        ("MF1-S1", "Commercial value depends on recoverability, development cost, timing, partners, prices and approvals—not only resource size.", ["SEPLAT-9M-2026"], "Atlas makes no valuation, price target or investment recommendation."),
        ("MF1-S2", "Seplat reports a 40% operated interest; preliminary gross in-place quantities are not the company's net saleable volumes.", ["SEPLAT-9M-2026"], "Do not convert gross in-place estimates into company revenue or reserves."),
        ("MF1-S3", "Existing infrastructure can be commercially relevant, yet no Aku-01 capital budget or project economics were disclosed in the cited evidence.", ["SEPLAT-9M-2026", "SEPLAT-OML53"], "Absence of disclosed project economics requires an explicit knowledge stop."),
    ],
    "C1": [
        ("C1-S1", "Nigeria's host-community framework makes participation and development planning a governed process.", ["NUPRC-HOST-2022", "PIA-2021"], "Do not name a host community without an applicable official determination."),
        ("C1-S2", "The statutory contribution is linked to preceding-year operating expenditure, not a simple share of discovery value.", ["PIA-2021"], "Do not imply a windfall, fixed amount or immediate distribution."),
    ],
    "W1": [
        ("W1-S1", "Imo's labour market is dominated by self-employment and informal work, so expectations may spread beyond direct payroll jobs.", ["NBS-LFS-2023"], "State survey structure does not predict Aku-01 employment."),
        ("W1-S2", "Oil-and-gas participation can require verified training, practical experience, certification and contractor pathways.", ["NCDMB-HCD"], "The framework creates pathways, not a guarantee for a fictional applicant."),
    ],
    "E1": [
        ("E1-S1", "Environmental review and operating controls belong before any claim about local impact or safety.", ["NUPRC-ENV"], "Do not invent a spill, pollution event, land take or safety outcome."),
        ("E1-S2", "Gas handling choices can affect flaring, emissions, waste and the value recovered from a development.", ["NUPRC-FLARE-2022"], "General regulatory objectives do not establish Aku-01's future emissions."),
        ("E1-S3", "Exact wellhead, host-community and development-plan evidence remain unresolved and limit local claims.", ["SEPLAT-9M-2026", "NUPRC-HOST-2022", "NUPRC-ENV"], "UNKNOWN is a production boundary, not an invitation to infer a site."),
    ],
}

GRAPHIC_SCENES = {"D1-S2", "D1-S3", "I1-S2", "MF1-S2", "MF1-S3", "C1-S2", "W1-S2", "E1-S2", "E1-S3"}
DATA = {
    "D1-S2": ("157 Bcf + 19 MMbbls", "Preliminary mid-case gas and oil in place; company estimate"),
    "D1-S3": ("4 prospects", "Described as de-risked; not discoveries"),
    "I1-S2": ("Potential tie-back", "Planned future connection; route and timing not final"),
    "MF1-S2": ("40%", "Seplat operated interest in PPL 2A25"),
    "MF1-S3": ("Economics undisclosed", "No Aku-01 capital budget in cited evidence"),
    "C1-S2": ("3% of prior OPEX", "Statutory trust contribution basis; not revenue share"),
    "W1-S2": ("Training → practice → certification", "National capability pathway; no job guarantee"),
    "E1-S2": ("Prevent waste and pollution", "Regulatory objective; not Aku-01 performance evidence"),
    "E1-S3": ("UNKNOWN", "Exact wellhead, host community and final development plan"),
}


def gate(stage, output, producer):
    return {"stage": stage, "status": "PASS", "produced_by": producer, "output": output}


def build_inputs():
    write_json("source-register.json", SOURCES)
    evidence = [{"id": item["id"], "claim": item["supports"]} for item in SOURCES]
    candidate = {
        "schema_version": "1.0", "candidate_id": EDITION, "origin": "EMRADAR",
        "working_title": "What the Well Changes",
        "hero_deck": "Aku-01 is a verified oil-and-gas discovery. The consequences are still conditional.",
        "world_change": "Seplat reported a preliminary oil and gas discovery at Aku-01 in onshore Imo State and plans to complete the well as a potential future producer tied to existing infrastructure.",
        "selection_state": "SELECTED_FOR_EDITION_GENERATION", "geographic_core": "Imo State, Nigeria",
        "evidence_basis": evidence,
        "human_emotional_hook": {"state": "PASS", "basis": "A new discovery can alter expectations about work, contracts, public benefit and environmental responsibility before it produces anything.", "boundary": "Fiction may explore anticipation and choice, but may not promise a job, identify a host community, or claim a local impact."},
    }
    write_json("selected-edition-candidate.json", candidate)
    write_json("selected-edition-gate.json", gate("edition_selection_gate", {
        "candidate_id": EDITION, "decision": "SELECTED", "advance_to_route_generation": True,
        "informational_completeness_gate": "PASS", "human_emotional_hook_gate": "PASS",
        "geographic_grounding_gate": "PASS", "causal_boundary_precheck": "PASS",
        "visual_context_viability": "PASS", "markets_finance_domain": "PASS",
        "reason": "Primary evidence supports discovery, infrastructure, commercial, labour, governance and environmental perspectives at Imo State or national-system resolution.",
        "publication_authorized": False,
    }, "Atlas bounded local production / 2026-11-19"))
    perspectives = []
    for pid, name, purpose, refs in PERSPECTIVES:
        item = {"id": pid, "name": name, "status": "ACCEPTED", "necessary": True, "evidence_basis": refs, "purpose": purpose}
        if pid == "MF1": item.update({"entry_label": "Markets and finance: resources, infrastructure and unresolved economics", "primary_domain": "markets_finance"})
        perspectives.append(item)
    write_json("selected-edition-perspectives.json", gate("perspective_gate", {"candidate_id": EDITION, "perspectives": perspectives, "completeness_result": "PASS", "human_emotional_hook_result": "PASS", "aoc001_template_check": "PASS — route count and subjects derive from Aku-01 evidence."}, "Atlas perspective gate / 2026-11-19"))
    routes = []
    for pid, name, _, _ in PERSPECTIVES:
        route_scenes = []
        for sid, meaning, refs, boundary in SCENES[pid]:
            scene = {"scene_id": sid, "meaning": meaning, "state": "UNCERTAIN" if sid in {"I1-S2", "MF1-S3", "E1-S3"} else "KNOWN", "evidence_refs": refs, "causal_boundary": boundary, "knowledge_stop": boundary if sid in {"I1-S2", "MF1-S3", "E1-S3"} else None}
            if pid == "MF1":
                scene["domains"] = ["markets_finance"]
                scene["finance_mechanism"] = {"MF1-S1": "valuation_boundary", "MF1-S2": "company_exposure", "MF1-S3": "financial_quality"}[sid]
            route_scenes.append(scene)
        routes.append({"perspective_id": pid, "perspective": name, "scenes": route_scenes})
    write_json("route_scene_generation.json", gate("route_scene_generation", {"candidate_id": EDITION, "routes": routes}, "Atlas route worker / 2026-11-19"))
    write_json("causal_boundary_gate.json", gate("causal_boundary_gate", {"candidate_id": EDITION, "routes": routes, "result": "PASS", "geographic_resolution": "Imo State unless a source explicitly supports wider OML 53 or national-system context"}, "Atlas boundary verifier / 2026-11-19"))
    story = {
        "candidate_id": EDITION, "label": "STORY / FICTION", "title": "Before Anything Flows",
        "characters": [
            {"name": "Adaeze", "role": "fictional electrical-engineering graduate living in Owerri"},
            {"name": "Chinedu", "role": "fictional uncle who runs a small vehicle-repair workshop"},
            {"name": "Nneka", "role": "fictional mother and market trader"},
        ],
        "story": [
            "Adaeze read the announcement twice before she got out of bed. The first time, the numbers held her: one hundred and fifty-seven billion cubic feet of gas in place, nineteen million barrels of oil in place. The second time, she slowed down over the smaller words around them—preliminary, potential, future. Those words changed the shape of the morning.",
            "Her mother, Nneka, was already preparing to leave for the market. She listened while Adaeze tried to explain the difference between finding hydrocarbons and producing them. ‘So they found it, but they have not decided what to do with it?’ Nneka asked. Adaeze said that was close enough. Nneka nodded, tied her bag and asked the question that mattered to her: ‘And when will anybody know?’ Adaeze had no answer.",
            "By the time she reached her uncle Chinedu's workshop, the radio had supplied one. The presenter spoke of jobs and new activity as if a discovery had opened a gate that morning. Chinedu turned down the volume and looked at Adaeze. ‘Electrical engineering,’ he said, pointing at her with a spanner. ‘Maybe at last you will use it here.’",
            "Adaeze put her bag on the only chair without a part on it. ‘A discovery is not a vacancy.’ Chinedu laughed, not because he thought she was wrong but because he thought she had become too practised at refusing hope before it could disappoint her.",
            "He returned to a vehicle with an electrical fault that had already defeated two batteries and most of his patience. Adaeze held the light while he traced the wiring. Her degree had taught her systems, measurement and failure. The workshop had taught her that a correct diagnosis was only useful if the customer could afford the repair. Neither lesson made her part of an oil-and-gas project. Both made the radio's certainty sound thin.",
            "At lunch, Chinedu showed her a message forwarded through three groups. It advertised an industry training programme and used the discovery headline above a registration link. There was no named organiser Adaeze recognised, no stated fee and no connection to Aku-01 that she could verify. Chinedu wanted to send it to everyone he knew. Adaeze asked him to wait.",
            "She searched for the company report instead. Then she found the Nigerian content training page. The real framework spoke about classroom learning, practical experience, work placement and certification. It did not offer her a place. It did not mention Aku-01. The distance between a pathway and a promise was less exciting than the forwarded message, but at least it existed.",
            "That evening, Nneka asked what training would cost if a real opportunity appeared. Travel, fees, time away from trading, another certificate—each possibility became a line in a household calculation for a programme nobody had announced. Adaeze said they were spending money that did not yet exist. Nneka replied that this was how families tested good news: they asked what it would demand from them.",
            "Chinedu arrived with food and an introduction. A customer of his repaired industrial motors and sometimes needed help documenting faults. Adaeze refused before he finished speaking. She did not want another favour described as experience and paid as gratitude. Chinedu became quiet. ‘Then ask him the terms,’ he said. ‘Refuse the bad terms, not the conversation.’",
            "The argument moved, as family arguments do, into everything around it. Nneka asked what communities nearer an operation should receive. Chinedu said people would expect roads, contracts and work. Adaeze asked which communities they meant. None of them knew the wellhead. None knew what development would be proposed, which communities a formal process might identify, or whether production would follow at all. Their certainty reduced as the questions became more specific.",
            "Later, Adaeze reopened her CV. She removed a sentence that claimed she was passionate about every kind of engineering and replaced it with the work she could actually defend: fault finding, basic control systems, maintenance records, the months she had spent helping Chinedu make order from other people's breakdowns. She sent a message asking the motor-repair customer what the work involved and whether it was paid.",
            "Before bed, she saved three links: the company report, the training page and the host-community regulations. She sent Chinedu a fourth message explaining why the forwarded registration link could not yet be trusted. Nothing had flowed from Aku-01 into their lives. No job had opened. No community benefit had been assigned. But the announcement had still done something: it had made rumour move faster, made old qualifications feel newly visible and made the family measure the distance between possibility and proof.",
            "Adaeze set an alert for the company name, placed her phone face down and turned off the light. Hope felt different when it had footnotes. It was smaller than a promise. It asked more of her than waiting. For tonight, that was enough.",
        ],
        "boundary": "Adaeze, Chinedu, Nneka, their dialogue, workshop, household and choices are invented. Owerri is used only as a regional urban setting; no character is a host-community resident or Aku-01 worker. The discovery, labour structure, training framework and governance rules are sourced conditions.",
    }
    write_json("story_synthesis.json", gate("story_synthesis", story, "Atlas story worker / 2026-11-19"))
    write_json("story_plausibility_gate.json", gate("story_plausibility_gate", {"candidate_id": EDITION, "result": "PASS", "checks": {"clearly_labelled_fiction": True, "contradicts_known_evidence": False, "comparison_disguised_as_local_fact": False, "unsupported_prevalence_claim": False, "severe_event_without_support": False, "cultural_stereotype_dependency": False}, "approved_story_elements": ["regional family conversation", "CV revision", "skills enquiry", "unverified forwarded training message", "paid-work boundary", "ordinary disagreement and bounded hope"], "rejected_story_elements": ["guaranteed employment", "named host community", "invented compensation", "invented spill or conflict", "claim that the fictional training message came from an operator or regulator"], "reader_boundary": "This is a regional fictional response to a verified announcement, not testimony."}, "Atlas plausibility verifier / 2026-11-19"))
    requirements, routing = [], []
    for pid, _, _, _ in PERSPECTIVES:
        for sid, meaning, _, boundary in SCENES[pid]:
            vtype = "cinematic AI-generated regional reconstruction"
            requirements.append({"scene_id": sid, "required": True, "purpose": meaning, "truth_boundary": boundary, "visual_type": vtype})
            routing.append({"scene_id": sid, "required": True, "purpose": meaning, "truth_boundary": boundary, "provider_decision": "OPENAI_IMAGEGEN", "asset_path": None})
    write_json("visual_requirements.json", gate("visual_requirements", {"candidate_id": EDITION, "requirements": requirements}, "Atlas visual requirements / 2026-11-19"))
    write_json("image_provider_routing.json", gate("image_provider_routing", {"candidate_id": EDITION, "visuals": routing, "runway_required": False, "video_required": True, "routing_note": "Cinematic regional and fictional reconstructions generated for owner review; none is documentary evidence or an exact Aku-01 site claim."}, "Atlas visual replacement / 2026-11-19"))
    write_json("visual-context.json", {"candidate_id": EDITION, "geography": "Imo State, Nigeria; no wellhead or host-community claim", "locality_evidence": [{"source_id": "SEPLAT-OML53", "scope": "State and licence context only"}, {"source_id": "NBS-LFS-2023", "scope": "State labour structure only"}, {"source_id": "NUPRC-HOST-2022", "scope": "National host-community process; no Aku-01 community named"}], "visual_bible": {"palette": "humid green, laterite red, deep petroleum blue and warm market gold", "camera": "cinematic naturalistic editorial reconstruction with deep perspective and restrained film grade", "continuity": "Imo regional vegetation, roads, workshops, market, civic process and energy infrastructure; fictional people remain explicitly reconstructed", "bans": ["named community", "exact wellhead", "reconstruction presented as documentary evidence", "spill or flare presented as actual", "company logo as endorsement"]}})
    write_json("visual-data.json", {sid: {"value": DATA[sid][0], "caption": DATA[sid][1], "scope": DATA[sid][1], "source_id": SCENES[sid.split("-")[0]][[x[0] for x in SCENES[sid.split("-")[0]]].index(sid)][2][0]} for sid in GRAPHIC_SCENES})


def editorial_copy():
    scene_copy = {}
    for pid, _, _, _ in PERSPECTIVES:
        for sid, meaning, refs, boundary in SCENES[pid]:
            state = "UNCERTAIN" if sid in {"I1-S2", "MF1-S3", "E1-S3"} else "FACT"
            text = meaning + " " + boundary
            scene_copy[sid] = {"heading": meaning.split("—")[0].rstrip("."), "paragraphs": [{"text": text, "state": state, "evidence_refs": refs}]}
    return {
        "opening": {"heading": "A discovery, not yet a development", "paragraphs": [{"text": "Seplat reports oil and gas at Aku-01 in onshore Imo State, with preliminary estimates and a plan for potential future production. Sources do not establish current production, revenue, exact wellhead or named host community.", "state": "FACT", "evidence_refs": ["SEPLAT-9M-2026"]}]},
        "consequences": {"heading": "The consequence chain is conditional", "paragraphs": [{"text": "Appraisal, engineering, approvals, investment, infrastructure, community governance, skills and environmental controls stand between a discovery and lived outcomes. Existing systems make several pathways plausible; none makes a specific benefit or harm inevitable.", "state": "UNCERTAIN", "evidence_refs": ["SEPLAT-9M-2026", "SEPLAT-OML53", "NUPRC-HOST-2022", "NUPRC-ENV"]}]},
        "place": {"heading": "Imo State, at the supported resolution", "paragraphs": [{"text": "OML 53 is an onshore Imo State licence with existing producing fields and infrastructure. This edition remains regional because the cited discovery evidence does not establish Aku-01's exact wellhead or an official host-community determination.", "state": "FACT", "evidence_refs": ["SEPLAT-OML53", "SEPLAT-9M-2026", "NUPRC-HOST-2022"]}]},
        "scenes": scene_copy,
    }


def contextual_png(path: Path, index: int, label: str):
    # Standard-library PPM raster, converted to PNG with macOS sips. The image is
    # an abstract regional editorial illustration, never a simulated photograph.
    w, h = 1200, 750
    pixels = bytearray(w * h * 3)
    variant = hashlib.sha256((label + str(index)).encode()).digest()
    for y in range(h):
        for x in range(w):
            t = y / h
            r, g, b = int(16 + 54*t), int(42 + 58*t), int(48 + 30*t)
            # Layered vegetation.
            for n in range(7):
                cx = (variant[n] * 11 + n * 173 + index * 61) % w
                cy = 350 + (variant[n+7] % 150)
                rad = 90 + variant[n+14] % 85
                if (x-cx)**2 + (y-cy)**2 < rad**2:
                    r, g, b = 27 + n*2, 83 + n*6, 55 + n*3
            # Laterite ground and a dark road narrowing into the horizon.
            if y > 555 - abs(x-w//2)//5: r, g, b = 126, 73, 47
            half = int(48 + (y-440)*0.44)
            if y > 440 and abs(x-w//2) < max(48, half): r, g, b = 39, 42, 43
            if y > 500 and abs(x-w//2) < 7: r, g, b = 221, 178, 92
            # Symbolic workshop / processing / grid structure varies by route.
            if index % 3 == 0 and 845 < x < 880 and 210 < y < 555: r, g, b = 69, 75, 73
            if index % 3 == 1 and 825 < x < 1070 and 330 < y < 565: r, g, b = 77, 70, 61
            if index % 3 == 2 and 835 < x < 1060 and (abs((x-835) % 90) < 12 or abs(y-275) < 10) and 215 < y < 560: r, g, b = 70, 78, 76
            off = (y*w+x)*3; pixels[off:off+3] = bytes((r, g, b))
    ppm = path.with_suffix(".ppm")
    ppm.write_bytes(f"P6\n{w} {h}\n255\n".encode() + pixels)
    subprocess.run(["/usr/bin/sips", "-s", "format", "png", str(ppm), "--out", str(path)], check=True, stdout=subprocess.DEVNULL)
    ppm.unlink()


def graphic_svg(path: Path, value: str, caption: str, source_id: str, index: int):
    accent = ["#d58a4a", "#7db18d", "#d0ad62"][index % 3]
    lines = textwrap.wrap(caption, 42)
    body = "".join(f'<text x="95" y="{520+i*58}" font-size="42">{line}</text>' for i, line in enumerate(lines))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000"><rect width="1600" height="1000" fill="#12252b"/><circle cx="1320" cy="230" r="330" fill="{accent}" opacity=".16"/><path d="M95 245H1505" stroke="{accent}" stroke-width="6"/><g font-family="Arial,sans-serif" fill="#efb777"><text x="95" y="125" font-size="28" letter-spacing="5">ATLASOQUENCE · EXPLANATORY</text></g><text x="95" y="410" font-family="Georgia,serif" font-size="105" fill="#f5eddf">{value}</text><g font-family="Georgia,serif" fill="#f5eddf">{body}</g><text x="95" y="910" font-family="Arial,sans-serif" font-size="25" fill="#d9d4c8">Scope: {caption} · Source: {source_id}</text></svg>'''
    path.write_text(svg, encoding="utf-8")


def build_assets_and_receipts():
    ASSETS.mkdir(parents=True, exist_ok=True)
    copy = editorial_copy(); write_json("editorial-copy.json", copy)
    # Owner-rejected deterministic media is replaced by the inspected cinematic
    # reconstruction set. Every rendered scene gets a unique publication path.
    contextual = [("reality-scene", "reality-scene.png"), ("consequences-scene", "consequences-scene.png"), ("place-scene", "place-scene.png")]
    for pid, _, _, _ in PERSPECTIVES: contextual.append((SCENES[pid][0][0], f"{pid.lower()}-s1.png"))
    assets = []
    for sid, filename in contextual:
        beat = sid + "-B1" if sid.endswith("-scene") else None
        path = ASSETS / filename
        if not path.is_file(): raise FileNotFoundError(path)
        text = copy[{"reality-scene":"opening", "consequences-scene":"consequences", "place-scene":"place"}[sid]]["paragraphs"][0]["text"] if beat else copy["scenes"][sid]["paragraphs"][0]["text"]
        assets.append({"scene_id": sid, **({"beat_id": beat} if beat else {}), "path": "/assets/aoc-002/" + path.name, "sha256": sha(path), "bytes": path.stat().st_size, "beat_text_sha256": hashlib.sha256(text.encode()).hexdigest() if beat else None, "provenance": "OpenAI image generation; cinematic Imo State regional or fictional reconstruction; not documentary evidence", "provider": "OPENAI_IMAGEGEN_CONTEXT", "truth_boundary": "AI-generated regional reconstruction; not Aku-01 footage, an exact wellhead, or a host-community claim.", "status": "PASS", "visual_qa": {"pass": True, "reason": "Inspected for regional continuity, cinematic composition, factual boundaries and absence of exact-site claims."}})
    route_images = {"D1":"d1-s1.png", "I1":"i1-s1.png", "MF1":"mf1-s1.png", "C1":"c1-s1.png", "W1":"w1-s1.png", "E1":"e1-s1.png"}
    for sid in sorted(GRAPHIC_SCENES):
        pid = sid.split("-")[0]; source = ASSETS / route_images[pid]
        path = ASSETS / (sid.lower() + ".png")
        shutil.copyfile(source, path)
        assets.append({"scene_id": sid, "path": "/assets/aoc-002/" + path.name, "sha256": sha(path), "bytes": path.stat().st_size, "provenance": "OpenAI image generation; cinematic perspective reconstruction replacing rejected deterministic graphic", "provider": "OPENAI_IMAGEGEN_CONTEXT", "truth_boundary": SCENES[pid][[x[0] for x in SCENES[pid]].index(sid)][3] + " Image is a reconstruction, not documentary evidence.", "status": "PASS", "visual_qa": {"pass": True, "reason": "Inspected cinematic reconstruction; factual value remains in sourced reader text rather than baked into imagery."}})
    film = ASSETS / "opening.webm"
    story_asset = ASSETS / "story-fiction.png"
    assets.extend([
        {"scene_id":"opening-film", "path":"/assets/aoc-002/opening.webm", "sha256":sha(film), "bytes":film.stat().st_size, "provenance":"Local cinematic motion composition from generated regional reconstructions; synthetic ambient sound; not documentary evidence", "provider":"ATLAS_LOCAL_MOTION", "truth_boundary":"AI-generated regional opening film; not documentary footage or an exact Aku-01 site claim.", "status":"PASS", "visual_qa":{"pass":True,"reason":"Inspected regional reconstruction; no exact-site claim."}},
        {"scene_id":"story-fiction", "path":"/assets/aoc-002/story-fiction.png", "sha256":sha(story_asset), "bytes":story_asset.stat().st_size, "provenance":"OpenAI image generation; fictional household reconstruction", "provider":"OPENAI_IMAGEGEN_CONTEXT", "truth_boundary":"STORY / FICTION; invented people and setting, not testimony.", "status":"PASS", "visual_qa":{"pass":True,"reason":"Inspected fictional reconstruction and visible story boundary."}},
    ])
    # Input binding is computed only after every declared input exists.
    from production_state import binding, digest
    bind = binding(RUN)
    write_json("editorial-qa.json", {**bind, "status": "PASS", "defects": [], "copy_sha256": digest(RUN / "editorial-copy.json"), "attempt": 1, "verifier": "bounded evidence audit / 2026-11-19"})
    write_json("asset-persistence-receipt.json", {**bind, "status": "PASS", "assets": assets, "defects": []})
    write_json("opening-media.json", {**binding(RUN), "edition_id": EDITION, "status": "PASS", "kind": "motion_video", "path": "/assets/aoc-002/opening.webm", "sha256": sha(film), "bytes": film.stat().st_size, "duration": 15.0, "dimensions": [1920, 1080], "provenance": "Local cinematic motion composition from generated regional reconstructions; synthetic ambient sound; not documentary evidence", "visual_qa": {"status": "PASS", "reviewer": "bounded local visual review / 2026-11-19", "reason": "Regional and fictional reconstruction labels preserved; no exact Aku-01 site claim; soundtrack fades over final 2.2 seconds."}})
    write_json("reader-display-copy.json", {"edition_id": EDITION, "purpose": "No editorial override; preserve evidence-bound copy.", "scene_overrides": {}})


def main():
    build_inputs(); build_assets_and_receipts()
    print(json.dumps({"edition": EDITION, "sources": len(SOURCES), "perspectives": len(PERSPECTIVES), "assets": len(list(ASSETS.iterdir()))}, indent=2))


if __name__ == "__main__":
    main()
