#!/usr/bin/env python3
"""Measure visible time-to-first-token locally, without saving chat history."""
import argparse
import json
import time
import urllib.request

p=argparse.ArgumentParser()
p.add_argument('model')
p.add_argument('--prompt',default='Hello! Reply with one short sentence.')
p.add_argument('--keep-alive',default='10m')
p.add_argument('--no-think',action='store_true')
a=p.parse_args()
body={'model':a.model,'messages':[{'role':'user','content':a.prompt}],'stream':True,'options':{'num_ctx':4096,'num_predict':128},'keep_alive':a.keep_alive}
if a.no_think:body['think']=False
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
req=urllib.request.Request('http://127.0.0.1:11434/api/chat',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
start=time.monotonic();first=None;reasoning=None;content='';last={}
with opener.open(req,timeout=120) as response:
    for line in response:
        item=json.loads(line)
        if item.get('error'):raise RuntimeError(item['error'])
        message=item.get('message',{})
        if message.get('thinking') and reasoning is None:reasoning=time.monotonic()-start
        if message.get('content'):
            if first is None:first=time.monotonic()-start
            content+=message['content']
        last=item
elapsed=time.monotonic()-start
print(json.dumps({'model':a.model,'first_visible_token_s':round(first,3) if first is not None else None,'first_reasoning_token_s':round(reasoning,3) if reasoning is not None else None,'total_s':round(elapsed,3),'load_s':round(last.get('load_duration',0)/1e9,3),'output_tokens':last.get('eval_count'),'tokens_per_s':round(last.get('eval_count',0)/(last.get('eval_duration',1)/1e9),1),'response':content,'context':4096,'no_think_requested':a.no_think},ensure_ascii=False))
