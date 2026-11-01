#!/usr/bin/env python3
"""Download two small models and create tuned aliases. Downloads total about 6 GB."""
import json
import urllib.request
import sys

MODELS=[('qwen3:4b-instruct','home-fast','Fast everyday bilingual text chat'),('gemma3:4b','home-vision','Small text and image model')]
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
def request(path,body):
    req=urllib.request.Request('http://127.0.0.1:11434'+path,data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
    return opener.open(req,timeout=600)

def main():
    for base,alias,description in MODELS:
        print('Downloading '+base,flush=True)
        last=-1
        with request('/api/pull',{'model':base,'stream':True}) as response:
            for line in response:
                data=json.loads(line)
                if data.get('error'):raise RuntimeError(data['error'])
                total=data.get('total',0)
                if total>100_000_000:
                    progress=int(data.get('completed',0)*100/total)//10*10
                    if progress!=last: print(f'  {progress}%',flush=True);last=progress
                elif data.get('status')=='success':print('  downloaded',flush=True)
        with request('/api/create',{'model':alias,'from':base,'parameters':{'num_ctx':16384,'num_predict':2048,'temperature':0.6},'stream':False}) as response:
            data=json.load(response)
            if data.get('error'):raise RuntimeError(data['error'])
        print(f'Ready: {alias} — {description}',flush=True)
    print('Select home-fast in Open WebUI for text, or home-vision for images. Aliases reuse the downloaded weights.',flush=True)
if __name__=='__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError) as error:
        sys.exit(f'Model setup stopped: {error}\nCheck Ollama and your network, then rerun this script. Ollama reuses partial downloads.')
