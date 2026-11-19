"""Evidence-backed Markets/Finance completeness for EMRADAR-origin editions."""
import re
from pathlib import Path
from production_state import read, write, binding

DOMAIN = 'markets_finance'
SIGNALS = re.compile(r'\b(investment|investing|capital|payback|repay|finance|financial|market|macro(?:economic)?|economic|productivity|income|afford|cost|returns?)\b', re.I)
MECHANISMS = {'economic_exposure','capital_and_payback','allocation_and_uncertainty',
              'supply_demand','company_exposure','financial_quality','valuation_boundary'}


def plan(run, routes):
    """Find existing evidence for a proposed domain route; never invent its copy."""
    by_route = []
    for route in routes:
        for scene in route['scenes']:
            if SIGNALS.search(scene['meaning']):
                by_route.append({'source_scene': scene['scene_id'],
                                 'intent': scene['meaning'],
                                 'evidence_refs': scene['evidence_refs'],
                                 'boundary': scene.get('causal_boundary')})
    categories=(('economic_exposure',r'workdays|income|economic|productivity'),
                ('capital_and_payback',r'investment|repay|payback|capital|cost'),
                ('allocation_and_uncertainty',r'afford|distribution|bears|uncertain|unresolved'))
    outline=[]
    for kind,pattern in categories:
        lead=next((item for item in by_route if re.search(pattern,item['intent'],re.I)
                   and item['source_scene'] not in {x['source_scene'] for x in outline}),None)
        if lead:outline.append({'mechanism':kind,**lead})
    return {'domain': DOMAIN, 'suggested_name': 'The Economics of '+
            ('Cooling' if any('cooling' in x['intent'].lower() for x in by_route) else 'Change'),
            'evidence_leads': by_route,
            'route_outline':outline,
            'financial_evidence_missing':['named company exposure','current financial quality',
                                          'valuation and entry price','investable security conclusion'],
            'required_work': 'Select an evidence-backed financial route; write and independently verify distinct scenes for capital/cost, market mechanism and financial uncertainty. Do not infer securities, valuations or returns from structural exposure.',
            'status': 'RESELECT_REQUIRED'}


def validate(run, routes):
    candidate = read(run/'selected-edition-candidate.json')
    sweep = Path(run)/'emradar-candidate-sweep.json'
    emradar = candidate.get('origin') == 'EMRADAR' or (sweep.exists() and any(
        x.get('id') == candidate['candidate_id'] for x in read(sweep).get('candidates', [])))
    if not emradar:
        return {'status': 'NOT_APPLICABLE', 'domain': DOMAIN}
    selected = read(run/'selected-edition-perspectives.json')['output']['perspectives']
    selected_ids = {p['id'] for p in selected if p['status'] == 'ACCEPTED'
                    and p.get('primary_domain') == DOMAIN
                    and SIGNALS.search(p.get('entry_label',p.get('name','')))}
    eligible = []
    for route in routes:
        if route['perspective_id'] not in selected_ids: continue
        # A passing domain is a real route with distinct financial mechanisms,
        # not a finance word attached to a human-consequence or solution route.
        financial = [s for s in route['scenes'] if s.get('evidence_refs') and
                     DOMAIN in s.get('domains', []) and s.get('finance_mechanism') in MECHANISMS
                     and SIGNALS.search(s['meaning'])]
        if len(financial) >= 2 and len({s['finance_mechanism'] for s in financial}) >= 2:
            eligible.append(route['perspective_id'])
    result = {**binding(run), 'domain': DOMAIN,
              'status': 'PASS' if eligible else 'BLOCKED',
              'selected_perspectives': eligible,
              'proposal': None if eligible else plan(run, routes)}
    write(run/'markets-finance-coverage.json', result)
    if not eligible:
        raise ValueError('MARKETS_FINANCE_DOMAIN_GAP: evidence-backed Perspective selection must be repaired before production')
    return result
