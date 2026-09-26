#!/usr/bin/env python3
"""Build the deterministic AOC-001 Signal Library proof from locked Atlas sources."""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EDITION="AOC-001"
MASTER=ROOT/"content/AOC-001/master-edition-v0.1.md"
REGISTER=ROOT/"content/AOC-001/sources/publication-source-register-v0.1.md"
MANIFEST=ROOT/"content/AOC-001/edition-manifest-v0.1.yaml"
OUTPUT=ROOT/"content/AOC-001/distribution/signal-library-v0.1.json"
SECTION_CLASS={"WHAT'S REAL":"factual","STORY — FICTION":"fictional","CONSEQUENCES":"analytical","PLACE":"factual","SOURCES":"factual"}
RULES=[
("WHAT'S REAL","AI models are trained and run in data centres","physical_infrastructure",["SR-03"]),
("WHAT'S REAL","415 TWh of electricity in 2024","scale_statistic",["SR-01","SR-02"]),
("WHAT'S REAL","copper among the metals required","material_demand",["SR-04"]),
("WHAT'S REAL","58% of national copper production in 2025","regional_supply",["SR-05"]),
("WHAT'S REAL","266 thousand tonnes of fine copper in 2025","operation_context",["SR-07","SR-08"]),
("STORY — FICTION","More responsibility. Better money.","fictional_opportunity",[]),
("STORY — FICTION","For being able to choose.","fictional_household_value",[]),
("STORY — FICTION","The house began rearranging itself.","fictional_family_rhythm",[]),
("STORY — FICTION","What does providing for your family mean","fictional_guiding_question",[]),
("CONSEQUENCES","additional electricity demand","documented_mechanism",["SR-01","SR-02","SR-04"]),
("CONSEQUENCES","Antofagasta is already Chile's largest copper-producing region","documented_place_connection",["SR-05","SR-06"]),
("CONSEQUENCES","Opportunity can be a consequence too","analytical_consequence",[]),
("PLACE","166,334 people in Calama","population_context",["SR-09"]),
("PLACE","Calama is more than extraction","place_identity",["SR-13"]),
("PLACE","physically close to Calama on a map","work_home_geography",["SR-10","SR-11","SR-12"]),
("PLACE","More than 10,000 people were moved","historical_context",["SR-14","SR-15"]),
("PLACE","Lickanantay/Atacameño communities","cultural_boundary",["SR-16"])
]
TOPIC_MAP={"AI":["artificial intelligence","data centres","digital infrastructure"],"copper":["copper","mining","materials"],"Calama":["Calama","place","community"],"family":["family","work","household"],"electricity":["electricity","grid","infrastructure"],"Indigenous":["Indigenous context","culture","territory"]}
INDUSTRY_MAP={"AI":["technology","data centres"],"copper":["mining","copper"],"electricity":["energy","grid infrastructure"],"work":["mining labour"]}
AUDIENCE_MAP={"AI":["technology readers","infrastructure professionals"],"copper":["resources sector","investors","mining communities"],"Calama":["Chile/Antofagasta audiences","place-based readers"],"family":["workers and families","future-work audiences"],"Indigenous":["research/education audiences"]}
VALUE_MAP={"copper":["resource demand","supply-chain relevance"],"electricity":["infrastructure demand"],"AI":["digital-infrastructure growth"],"work":["labour/future-work relevance"]}

def sections(text):
    out={}; current=None
    for line in text.splitlines():
        if line.startswith("# ") and not line.startswith("## "):
            title=line[2:].strip(); current=title if title in SECTION_CLASS else None
            if current: out[current]=[]
        elif current: out[current].append(line)
    return {k:"\n".join(v) for k,v in out.items()}

def clean(s): return re.sub(r"\s+"," ",re.sub(r"[*_]","",s)).strip()

def containing_statement(body,needle):
    paras=[clean(p) for p in re.split(r"\n\s*\n",body) if clean(p)]
    for p in paras:
        if needle.lower() in p.lower():
            sentences=re.split(r"(?<=[.!?])\s+",p)
            return clean(next((x for x in sentences if needle.lower() in x.lower()),p))
    raise ValueError(f"missing locked source text: {needle}")

def tags(statement,mapping):
    low=statement.lower(); out=[]
    for key,vals in mapping.items():
        if key.lower() in low: out.extend(vals)
    return sorted(set(out))

def evidence_strength(c,refs):
    if c=="fictional": return "not_applicable_fiction"
    if refs: return "registered_evidence"
    return "analysis_from_registered_mechanism"

def risk(c,s):
    risks=[]
    if c=="fictional": risks.append("fact_fiction_boundary")
    if any(x in s.lower() for x in ("indigenous","lickanantay","atacameño")): risks.append("cultural_sensitivity")
    if any(x in s.lower() for x in ("invest","production","demand","copper")): risks.append("causal_overstatement")
    return risks or ["low"]

def main(check=False):
    master=MASTER.read_text(encoding="utf-8"); register=REGISTER.read_text(encoding="utf-8")
    sec=sections(master)
    if set(SECTION_CLASS)-set(sec): raise ValueError("master edition section scan incomplete")
    signals=[]
    for i,(section,needle,stype,refs) in enumerate(RULES,1):
        statement=containing_statement(sec[section],needle); c=SECTION_CLASS[section]
        for ref in refs:
            if f"## {ref} " not in register and f"**{ref}**" not in register: raise ValueError(f"{ref} missing from source register")
        if c=="fictional" and refs: raise ValueError("fiction signal cannot carry factual evidence refs")
        if c=="factual" and not refs: raise ValueError("factual signal requires evidence refs")
        geography=["global"] if section=="WHAT'S REAL" else ["Calama","Antofagasta Region","Chile"] if section in {"PLACE","STORY — FICTION"} else ["global","Antofagasta Region","Chile"]
        r=risk(c,statement)
        signals.append({
          "signal_id":f"AOC001-SIG-{i:03d}","edition_id":EDITION,"originating_section":section,"signal_statement":statement,
          "signal_type":stype,"classification":c,"evidence_refs":refs,"evidence_strength":evidence_strength(c,refs),
          "geography":geography,"topics":tags(statement,TOPIC_MAP),"affected_industries":tags(statement,INDUSTRY_MAP),
          "potential_audiences":tags(statement,AUDIENCE_MAP),"value_commercial_relevance":tags(statement,VALUE_MAP),
          "sensitivity_risk":r,"available_assets":["approved factual report video"] if c=="factual" and section=="WHAT'S REAL" else ["approved STORY / FICTION promo"] if c=="fictional" else [],
          "potential_depth":["short","medium","long"],"extraction_status":"proof_extracted","human_review_required":c!="factual" or r!=["low"],
          "provenance":{"master_edition":"content/AOC-001/master-edition-v0.1.md","source_register":"content/AOC-001/sources/publication-source-register-v0.1.md","edition_manifest":"content/AOC-001/edition-manifest-v0.1.yaml","source_text_sha256":hashlib.sha256(statement.encode()).hexdigest(),"rule_trigger":needle}
        })
    payload={"schema_version":"1.0","library_id":"AOC-001-signal-library-v0.1","edition_id":EDITION,"constitutional_rule":"Facts can change the fiction. Fiction must never quietly become fact.","inputs":{"master_edition":"content/AOC-001/master-edition-v0.1.md","source_register":"content/AOC-001/sources/publication-source-register-v0.1.md","edition_manifest":"content/AOC-001/edition-manifest-v0.1.yaml"},"generator":"tools/build_signal_library.py","signal_count":len(signals),"signals":signals}
    rendered=json.dumps(payload,indent=2,ensure_ascii=False)+"\n"
    if check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8")!=rendered:
            print("SIGNAL LIBRARY CHECK: FAIL - generated output differs"); return 1
        print(f"SIGNAL LIBRARY CHECK: PASS - {len(signals)} signals")
        print(f"- factual: {sum(s['classification']=='factual' for s in signals)}")
        print(f"- analytical: {sum(s['classification']=='analytical' for s in signals)}")
        print(f"- fictional: {sum(s['classification']=='fictional' for s in signals)}")
        print("- fiction evidence refs: 0"); return 0
    OUTPUT.write_text(rendered,encoding="utf-8"); print(f"Wrote {OUTPUT.relative_to(ROOT)} with {len(signals)} signals"); return 0
if __name__=="__main__": raise SystemExit(main("--check" in sys.argv))
