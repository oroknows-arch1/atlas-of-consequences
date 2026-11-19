"""Preserve actionable provider errors without disclosing API credentials."""
import json
import os
import re
from urllib.error import HTTPError

def describe(error):
    if not isinstance(error,HTTPError): return str(error)
    try:
        body=json.loads(error.read())
        detail=body.get('error',body)
        if isinstance(detail,dict):
            message='; '.join(f'{k}={detail[k]}' for k in ('type','code','param','message') if detail.get(k))
        else: message=str(detail)
    except Exception: message='Provider did not return a readable error body'
    for key in ('OPENAI_API_KEY','RENDER_API_KEY'):
        if os.environ.get(key): message=message.replace(os.environ[key],'[REDACTED]')
    message=re.sub(r'\bsk-[A-Za-z0-9_-]+','[REDACTED]',message)
    return f'Provider HTTP {error.code}: {message[:2000]}'


def requires_external_action(error):
    message=str(error).lower()
    return any(code in message for code in ('provider_route_blocked', 'moderation_blocked', 'invalid_api_key', 'insufficient_quota', 'billing_hard_limit_reached'))
