"""Bounded safe alternatives; never resubmit a rejected depiction or relax QA."""
import hashlib
import json
import os
from production_state import binding, read, write, require_current
from editorial_factory import model_json, object_schema

POLICY_VERSION = 'safe-visual-v2'

PROPOSAL=object_schema({'decision':{'type':'string','enum':['SAFE_ALTERNATIVE','BLOCKED']},
                       'composition':{'type':'string'},'reason':{'type':'string'}})
VERDICT=object_schema({'safe':{'type':'boolean'},'meaning_preserved':{'type':'boolean'},
                      'boundary_preserved':{'type':'boolean'},'reason':{'type':'string'}})

def request_asset(run,job,command,invoke):
    if os.environ.get('ATLAS_SAFE_VISUAL_REEXPRESSION')!='1':
        return invoke(command,job)
    path=run/'provider-routing-receipt.json'
    history=read(path) if path.exists() else {**binding(run),'scenes':{}}
    require_current(run,history)
    sid=job['scene_id']
    stable={k:v for k,v in job.items() if k not in ('attempt','repair_feedback')}
    key=hashlib.sha256(json.dumps(stable,sort_keys=True).encode()).hexdigest()
    record=history['scenes'].setdefault(sid,{'job_sha256':key,'original_job':stable,'events':[]})
    if record['job_sha256']!=key: raise RuntimeError('provider routing receipt belongs to a different visual job')
    if record.get('policy_version') != POLICY_VERSION:
        record['policy_version'] = POLICY_VERSION
        record.pop('alternative', None)
        record.pop('equivalence_qa', None)
        record.pop('safe_primary_rejected', None)
        record.pop('alternate_rejected', None)
        save_needed = True
    else:
        save_needed = False
    def save():write(path,history)
    # Import the actual earlier refusal; never submit that same rejected request again.
    previous=run/'asset-persistence-receipt.json'
    if not record['events'] and previous.exists():
        for defect in read(previous).get('defects',[]):
            if defect.get('scene_id')==sid and 'moderation_blocked' in defect.get('reason',''):
                record['events'].append({'kind':'original_rejection','provider':command,'reason':defect['reason'],'imported_from':'asset-persistence-receipt.json'})
                save()
    if save_needed: save()
    if not record['events']:
        try:return invoke(command,job)
        except RuntimeError as error:
            if 'moderation_blocked' not in str(error):raise
            record['events'].append({'kind':'original_rejection','provider':command,'reason':str(error)})
            save()
    if 'alternative' not in record:
        proposal=model_json('''A contextual image request was rejected by the provider. Do NOT evade safety
systems, disguise rejected content, or advise bypassing a refusal. Decide whether a genuinely safer,
ordinary environment-only illustration can serve the SAME accepted editorial purpose. No people, bodies, distress, illness, injury, violence or reenactment. Use buildings, airflow, objects
and ambient conditions only where relevant. For school/child consequences, use school objects such as
empty desks, closed exercise books, fans, shut classroom doors or empty corridors to communicate the
relationship between heat and disrupted schooling without depicting children or a specific closure. Do not invent a real incident or imply a documented closure/site.
Keep geography, evidence limits, scene meaning and truth boundary unchanged. Return BLOCKED if these
constraints cannot honestly fulfil the purpose. If possible propose ONE explicit composition, describing
what is shown, not instructions to the provider about moderation. No alternate factual claims.''',
                            {'original_job':stable},PROPOSAL)
        record['alternative']=proposal;save()
        if proposal['decision']=='SAFE_ALTERNATIVE':
            verdict=model_json('''Independently inspect the proposed materially safer visual composition.
Approve only ordinary environment/object imagery with no people, distress, injury, reenactment or
prohibited content. It must preserve the original scene's editorial meaning, geography, purpose and
truth boundary. It must not encode or conceal a rejected depiction. Contextual illustration is not
proof of an actual event. If the proposed visual loses the required meaning, return false. Do not
approve merely to complete production.''',{'original_job':stable,'proposal':proposal},VERDICT)
            record['equivalence_qa']=verdict;save()
    verdict=record.get('equivalence_qa',{})
    if record['alternative']['decision']!='SAFE_ALTERNATIVE' or not all(verdict.get(k) is True for k in ('safe','meaning_preserved','boundary_preserved')):
        raise RuntimeError('provider_route_blocked: no independently approved safe equivalent visual')
    # The provider and final visual verifier still receive the unchanged editorial job.
    safe_job=dict(job, safe_composition=record['alternative']['composition'],repair_feedback='')
    if not record.get('safe_primary_rejected'):
        try:
            result=invoke(command,safe_job)
            result['routing_provenance']={'receipt':'provider-routing-receipt.json','scene_id':sid,'route':'safe_equivalent_primary'}
            return result
        except RuntimeError as error:
            if 'moderation_blocked' not in str(error):raise
            record['safe_primary_rejected']=True
            record['events'].append({'kind':'safe_alternative_rejection','provider':command,'reason':str(error)})
            save()
    # An alternate is never invented or silently authorized. It receives only the
    # independently approved safer composition, not the originally rejected depiction.
    alternate=os.environ.get('ATLAS_APPROVED_ALTERNATE_IMAGE_COMMAND')
    if not alternate or record.get('alternate_rejected'):
        raise RuntimeError('provider_route_blocked: safe alternative refused; no available authorized alternate')
    try:
        result=invoke(alternate,safe_job)
        result['routing_provenance']={'receipt':'provider-routing-receipt.json','scene_id':sid,'route':'authorized_alternate'}
        return result
    except RuntimeError as error:
        record['alternate_rejected']=True
        record['events'].append({'kind':'alternate_rejection','provider':alternate,'reason':str(error)})
        save();raise RuntimeError('provider_route_blocked: authorized alternate failed: '+str(error)) from error
