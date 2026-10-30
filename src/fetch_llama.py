#!/usr/bin/env python3
"""Optional live DefiLlama *free* metrics snapshot; never claims derivatives volume is free."""
from __future__ import annotations
import argparse,datetime,json,urllib.request,urllib.error
from pathlib import Path
from urllib.parse import urlencode
ROOT=Path(__file__).resolve().parents[1]
ENDPOINTS={
    'fees':('overview/fees',dict(dataType='dailyFees',excludeTotalDataChart='true',excludeTotalDataChartBreakdown='true')),
    'revenue':('overview/fees',dict(dataType='dailyRevenue',excludeTotalDataChart='true',excludeTotalDataChartBreakdown='true')),
    'oi':('overview/open-interest',dict(excludeTotalDataChart='true',excludeTotalDataChartBreakdown='true')),
}
ALIASES=('sai','hyperliquid','gmx','dydx')
def extract(payload):
    matches=[]
    for p in payload.get('protocols',[]):
        n=str(p.get('name','')).lower()
        if any(w in n for w in ALIASES):
            matches.append(dict(name=p.get('name'),slug=p.get('slug'),total24h=p.get('total24h'),total7d=p.get('total7d'),total30d=p.get('total30d'),change_1d=p.get('change_1d'),methodology=p.get('methodology')))
    return matches

def capture(out, timeout=20):
    out.mkdir(parents=True,exist_ok=True)
    report={'captured_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Free API endpoints only; protocols with absent data must not be treated as zero','sources':{}}
    for label,(path,query) in ENDPOINTS.items():
        url='https://api.llama.fi/'+path+'?'+urlencode(query)
        req=urllib.request.Request(url,headers={'User-Agent':'CareerOS-Research-Prototype/0.1'})
        with urllib.request.urlopen(req,timeout=timeout) as response:
            body=json.load(response)
        report['sources'][label]={'url':url,'protocols':extract(body),'all_records':len(body.get('protocols',[]))}
    target=out/'live_metric_snapshot.json';target.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    return target
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--live',action='store_true',help='allow actual network requests');p.add_argument('--out',type=Path,default=ROOT/'artifacts');a=p.parse_args()
    if not a.live:
        print('NETWORK DISABLED BY DEFAULT. Use --live on a machine with Internet access. No figures fabricated.')
    else:
        try:print(capture(a.out))
        except (urllib.error.URLError,ValueError) as e:raise SystemExit('FETCH FAILED — no cached live metrics written: '+str(e))
