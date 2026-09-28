"""Regression tests for evidence-domain and rendered visual coverage."""
import copy
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from production_state import INPUTS, ROOT, read, write
from market_finance import validate as finance_validate
from visual_coverage import beats_for, plan as visual_plan


class FactoryCoverage(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.run=Path(self.temp.name)
        source=ROOT/'content/AUTOMATED-TEST-001'
        for name in INPUTS:shutil.copyfile(source/name,self.run/name)
        shutil.copyfile(source/'emradar-candidate-sweep.json',self.run/'emradar-candidate-sweep.json')
        self.routes=read(self.run/'causal_boundary_gate.json')['output']['routes']
        self.requirements=read(self.run/'visual_requirements.json')['output']['requirements']
        self.assets=read(source/'asset-persistence-receipt.json')['assets']
        self.copy=read(source/'editorial-copy.json')

    def test_emradar_cannot_pass_with_finance_mentions_buried_in_other_routes(self):
        with self.assertRaisesRegex(ValueError,'MARKETS_FINANCE_DOMAIN_GAP'):
            finance_validate(self.run,self.routes)
        proposal=read(self.run/'markets-finance-coverage.json')['proposal']
        self.assertEqual(proposal['status'],'RESELECT_REQUIRED')
        self.assertTrue(any(x['source_scene']=='H6-S2' for x in proposal['evidence_leads']))

    def test_named_investor_alone_does_not_satisfy_domain(self):
        selected=read(self.run/'selected-edition-perspectives.json')
        selected['output']['perspectives'][0].update(name='Investor',primary_domain='markets_finance')
        write(self.run/'selected-edition-perspectives.json',selected)
        with self.assertRaisesRegex(ValueError,'MARKETS_FINANCE_DOMAIN_GAP'):
            finance_validate(self.run,self.routes)

    def test_evidenced_finance_route_can_have_an_adaptive_name(self):
        selected=read(self.run/'selected-edition-perspectives.json')
        selected['output']['perspectives'][-1]['primary_domain']='markets_finance'
        selected['output']['perspectives'][-1]['entry_label']='Finance and adaptation'
        write(self.run/'selected-edition-perspectives.json',selected)
        route=self.routes[-1]
        for scene,mechanism in zip(route['scenes'][1:],['capital_and_payback','allocation_and_uncertainty']):
            scene['domains']=['markets_finance'];scene['finance_mechanism']=mechanism
        self.assertEqual(finance_validate(self.run,self.routes)['selected_perspectives'],['H6'])

    def test_existing_assets_are_preserved_and_missing_beats_are_reported(self):
        receipt=visual_plan(self.run,self.routes,self.requirements,self.assets,self.copy)
        self.assertEqual(receipt['status'],'BLOCKED')
        self.assertEqual(receipt['planned_beats']['H1-S1-B1']['asset_path'],'/assets/aet1-wc-002/h1-s1.png')
        self.assertTrue(any(g['beat_id']=='H1-S1-B2' for g in receipt['gaps']))
        self.assertEqual(receipt['required_count'],sum(len(beats_for(self.copy['scenes'][s['scene_id']]))
                     for r in self.routes for s in r['scenes'] if next(v for v in self.requirements if v['scene_id']==s['scene_id'])['required']))

    def test_distinct_coverage_passes_and_consecutive_repetition_fails(self):
        assets=copy.deepcopy(self.assets)
        for r in self.routes:
            for s in r['scenes']:
                spec=next(v for v in self.requirements if v['scene_id']==s['scene_id'])
                if not spec['required']:continue
                for i,(_,beat_text) in enumerate(beats_for(self.copy['scenes'][s['scene_id']]),1):
                    if i==1:continue
                    assets.append({'scene_id':s['scene_id'],'beat_id':f'{s["scene_id"]}-B{i}',
                                   'path':f'/assets/test/{s["scene_id"]}-B{i}.png','sha256':f'beat-{i}',
                                   'beat_text_sha256':__import__('hashlib').sha256(beat_text.encode()).hexdigest()})
        self.assertEqual(visual_plan(self.run,self.routes,self.requirements,assets,self.copy)['status'],'PASS')
        repeat=next(a for a in assets if a.get('beat_id')=='H1-S1-B2')
        repeat['path']=next(a for a in assets if a['scene_id']=='H1-S1' and not a.get('beat_id'))['path']
        self.assertIn('Consecutive image repetition',visual_plan(self.run,self.routes,self.requirements,assets,self.copy)['gaps'][0]['reason'])

    def test_more_edition_copy_changes_the_asset_plan_without_a_fixed_quota(self):
        before=visual_plan(self.run,self.routes,self.requirements,self.assets,self.copy)
        self.copy['scenes']['H1-S1']['paragraphs'][0]['text'] += ' A new verified sentence changes this scene and its visual intent.'
        after=visual_plan(self.run,self.routes,self.requirements,self.assets,self.copy)
        self.assertGreater(after['required_count'],before['required_count'])
        self.assertGreater(len(after['gaps']),len(before['gaps']))


if __name__=='__main__':unittest.main()
