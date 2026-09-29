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
from finance_route_worker import assemble
from produce_edition import produce_assets
from provider_routing import request_asset
from production_state import binding


class FactoryCoverage(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.run=Path(self.temp.name)
        source=ROOT/'content/AUTOMATED-TEST-001'
        for name in INPUTS:shutil.copyfile(source/name,self.run/name)
        # Construct the preselection state from the current accepted edition.
        # Production may append routes and assets after these regression tests
        # are written; that progress must not mutate the negative fixture.
        for name in ('route_scene_generation.json','causal_boundary_gate.json'):
            data=read(self.run/name)
            data['output']['routes']=[r for r in data['output']['routes'] if r['perspective_id']!='MF1']
            write(self.run/name,data)
        data=read(self.run/'selected-edition-perspectives.json')
        data['output']['perspectives']=[p for p in data['output']['perspectives'] if p['id']!='MF1']
        write(self.run/'selected-edition-perspectives.json',data)
        for name,key in (('visual_requirements.json','requirements'),('image_provider_routing.json','visuals')):
            data=read(self.run/name)
            data['output'][key]=[item for item in data['output'][key] if not item['scene_id'].startswith('MF1-')]
            write(self.run/name,data)
        data=read(self.run/'visual-data.json')
        for key in list(data):
            if key.startswith('MF1-'):del data[key]
        write(self.run/'visual-data.json',data)
        data=read(self.run/'selected-edition-gate.json')
        data['output']['markets_finance_domain']='pending_repair'
        write(self.run/'selected-edition-gate.json',data)
        shutil.copyfile(source/'emradar-candidate-sweep.json',self.run/'emradar-candidate-sweep.json')
        self.routes=read(self.run/'causal_boundary_gate.json')['output']['routes']
        self.requirements=read(self.run/'visual_requirements.json')['output']['requirements']
        # Keep the intentionally incomplete, pre-beat fixture stable as the
        # live edition accrues verified assets. Its legacy scene binaries are
        # real and remain subject to the same hash/provenance checks.
        self.assets=[a for a in read(source/'asset-persistence-receipt.json')['assets']
                     if not a['scene_id'].startswith('MF1-') and not a.get('beat_id')]
        self.copy=read(source/'editorial-copy.json')
        self.copy['scenes']={sid:scene for sid,scene in self.copy['scenes'].items() if not sid.startswith('MF1-')}
        from market_finance import plan
        write(self.run/'markets-finance-coverage.json',{'proposal':plan(self.run,self.routes)})

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
        self.assertTrue(any(g['beat_id']=='H3-S1-B1' for g in receipt['gaps']))
        self.assertEqual(receipt['required_count'],sum(len(beats_for(self.copy['scenes'][s['scene_id']]))
                     for r in self.routes for s in r['scenes'])+
                     sum(len(beats_for(self.copy[key])) for key in ('opening','place','consequences')))

    def test_distinct_coverage_passes_and_consecutive_repetition_fails(self):
        assets=copy.deepcopy(self.assets)
        for gap in visual_plan(self.run,self.routes,self.requirements,assets,self.copy)['gaps']:
            beat=gap['beat_id'];assets.append({'scene_id':gap['scene'],'beat_id':beat,
                   'path':f'/assets/test/{beat}.png','sha256':beat,
                   'beat_text_sha256':__import__('hashlib').sha256(gap['intent']['beat_text'].encode()).hexdigest()})
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

    def test_finance_assembly_uses_existing_evidence_and_adaptive_name(self):
        outline=read(self.run/'markets-finance-coverage.json')['proposal']['route_outline'] if (self.run/'markets-finance-coverage.json').exists() else __import__('market_finance').plan(self.run,self.routes)['route_outline']
        output={'name':'The Cooling Ledger','entry_label':'Finance and cooling',
                'scenes':[{'mechanism':x['mechanism'],'heading':'Evidence, costs and limits',
                           'paragraphs':[{'text':x['intent'],'state':'UNCERTAIN' if i==2 else 'FACT',
                                          'evidence_refs':x['evidence_refs']}],
                           'visual':{'required':True,'purpose':'Show the evidenced mechanism',
                                     'truth_boundary':x['boundary'],'visual_type':'editorial contextual still'}}
                          for i,x in enumerate(outline)]}
        route,perspective,blocks,requirements,routing,graphics=assemble(self.run,output,outline)
        self.assertEqual(perspective['primary_domain'],'markets_finance')
        self.assertEqual(len(route['scenes']),len(outline))
        self.assertEqual({x['scene_id'] for x in requirements},set(blocks))
        self.assertFalse(graphics)

    def test_changed_route_binding_keeps_unchanged_verified_binary_jobs(self):
        source=ROOT/'content/AUTOMATED-TEST-001'
        receipt=read(source/'asset-persistence-receipt.json')
        receipt['assets']=copy.deepcopy(self.assets)
        write(self.run/'asset-persistence-receipt.json',receipt)
        selected=read(self.run/'selected-edition-gate.json')
        selected['output']['markets_finance_domain']='pending_repair'
        write(self.run/'selected-edition-gate.json',selected)
        # The global fingerprint changed, but each old scene job and binary did not.
        import os
        from unittest.mock import patch
        with patch.dict(os.environ,{'ATLAS_IMAGE_COMMAND':'','ATLAS_VISUAL_QA_COMMAND':''}):
            assets,defects=produce_assets(self.run,'AET1-WC-002',self.routes,self.requirements,
                                          read(self.run/'selected-edition-candidate.json'))
        self.assertEqual(defects,[])
        self.assertEqual(len(assets),len(self.assets))
        self.assertEqual({a['sha256'] for a in assets},{a['sha256'] for a in self.assets})

    def test_provider_routing_rebinds_only_identical_jobs_after_route_selection(self):
        import os
        from unittest.mock import patch
        job={'scene_id':'H1-S1','meaning':'Accepted meaning'}
        old={**binding(self.run),'scenes':{'H1-S1':{'job_sha256':__import__('hashlib').sha256(
            __import__('json').dumps(job,sort_keys=True).encode()).hexdigest(),
            'original_job':job,'events':[],'policy_version':'safe-visual-v2'}}}
        write(self.run/'provider-routing-receipt.json',old)
        selected=read(self.run/'selected-edition-gate.json');selected['output']['markets_finance_domain']='PASS'
        write(self.run/'selected-edition-gate.json',selected)
        with patch.dict(os.environ,{'ATLAS_SAFE_VISUAL_REEXPRESSION':'1'}):
            result=request_asset(self.run,job,'test-provider',lambda command,payload:{'path':'verified'})
            self.assertEqual(result['path'],'verified')
            self.assertEqual(read(self.run/'provider-routing-receipt.json')['input_sha256'],binding(self.run)['input_sha256'])
            with self.assertRaisesRegex(RuntimeError,'different visual job'):
                request_asset(self.run,dict(job,meaning='Changed meaning'),'test-provider',lambda *a:None)


if __name__=='__main__':unittest.main()
