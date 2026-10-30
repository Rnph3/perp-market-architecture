#!/usr/bin/env python3
"""Build a source-traceable qualitative perp venue comparison. Python standard library only."""
from __future__ import annotations
import argparse, csv, json, re, html
from pathlib import Path

COLUMNS = ['name','execution','liquidity','collateral_and_settlement','funding_model','fee_mechanism','risk_focus','caveat','sources']

def validate(data:dict)->None:
    assert re.fullmatch(r'\d{4}-\d{2}-\d{2}',data['as_of'])
    protocols=data['protocols']; assert len(protocols)>=3
    assert len({p['name'] for p in protocols})==len(protocols), 'duplicate protocol names'
    for p in protocols:
        for k in COLUMNS[:-1]:
            assert isinstance(p[k],str) and p[k].strip(), f'{p.get("name", "?")} missing {k}'
        assert len(p['source_urls'])>=2
        assert all(x.startswith('https://') for x in p['source_urls'])

def rows(data:dict):
    for p in data['protocols']:
        d={k:p[k] for k in COLUMNS if k!='sources'};d['sources']='; '.join(p['source_urls'])
        yield d

def html_card(x,y,width,fill):
    title=html.escape(x['name']);desc=html.escape(x['execution'])
    def wrap(s,maxlen=38):
        words=s.split(); out=[]; current=''
        for w in words:
            if len(current)+len(w)+1>maxlen and current:out.append(current);current=w
            else:current=(current+' '+w).strip()
        if current:out.append(current)
        return out[:3]
    lines=wrap(desc)
    content=f'<rect x="{x["x"]}" y="{y}" rx="13" width="{width}" height="164" fill="{fill}" stroke="#243447" stroke-width="1"/>'
    content+=f'<text x="{x["x"]+20}" y="{y+38}" fill="#EAF5FF" font-family="sans-serif" font-size="20" font-weight="bold">{title}</text>'
    for i,l in enumerate(lines):content+=f'<text x="{x["x"]+20}" y="{y+68+i*18}" fill="#C7D8E8" font-family="sans-serif" font-size="12">{l}</text>'
    content+=f'<text x="{x["x"]+20}" y="{y+143}" fill="#7DD3FC" font-family="sans-serif" font-size="11">PRIMARY DOCS LINKED IN REPORT</text>'
    return content

def svg(data):
    protocol=data['protocols']; w=1180; sw=265; gap=20; margin=30
    body=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 275" role="img" aria-label="Perpetual DEX architectural mechanisms"><rect width="{w}" height="275" fill="#08131E"/><text x="30" y="38" fill="#F1F7FB" font-size="25" font-family="sans-serif" font-weight="bold">PerpDEX / Four Execution Architectures</text><text x="30" y="61" fill="#8CA4BB" font-size="13" font-family="sans-serif">Qualitative, sourced comparison · not a fee or return ranking</text>'
    fills=['#172B40','#1A293C','#233044','#1B3141']
    for i,p in enumerate(protocol):
        item=dict(p);item['x']=margin+i*(sw+gap)
        body+=html_card(item,86,sw,fills[i%len(fills)])
    return body+'</svg>'

def report(data):
    pp=data['protocols']; lines=[f'# Perpetual DEX Market Structure: Sai vs Hyperliquid vs GMX vs dYdX Chain',
      f'**Documentation snapshot:** {data["as_of"]}. **Type:** qualitative protocol research, NOT live financial performance.', '',
      '## Research question', data['research_question'],'',
      '## Executive summary',
      'The trading venue is not just its interface. An oracle-priced vault-backed venue exposes liquidity-provider inventory and oracle/settlement risks; an order-book venue shifts execution quality toward resting liquidity and matching mechanics. These are structural observations, not evidence that one design performs better.',
      '', '## Source-traceable design matrix',
      '| Venue | Execution | Backing liquidity | Funding/borrow | Principal risk |',
      '|---|---|---|---|---|']
    def safe(s):return s.replace('|','/')
    for p in pp:
        lines.append('| '+ ' | '.join(map(safe,[p['name'],p['execution'],p['liquidity'],p['funding_model'],p['risk_focus']]))+' |')
    lines+=['','## Venue-by-venue mechanics']
    for p in pp:
        lines+=['',f'### {p["name"]}', f'- **Execution:** {p["execution"]}.',f'- **Liquidity:** {p["liquidity"]}.',f'- **Collateral/settlement:** {p["collateral_and_settlement"]}.',f'- **Funding:** {p["funding_model"]}.',f'- **Fee mechanism:** {p["fee_mechanism"]}.',f'- **Researchable failure mode:** {p["risk_focus"]}.',f'- **Limitation:** {p["caveat"]}.', '**Primary sources:**']
        lines+=[f'  - {u}' for u in p['source_urls']]
    lines+=['','## Falsifiable follow-up questions',
      '1. For a fixed notional and liquidity regime, what is the realized all-in execution cost (including rapid-close penalties, funding, and price impact)?',
      '2. Under large price jumps, which mechanism absorbs losses: liquidity providers, resting orders, insurance/clearing, or liquidation cascades?',
      '3. How much execution quality varies with position holding horizon (30 seconds vs 30 minutes vs 1 day)?',
      '4. Which stated risk controls can be verified onchain or through public historical events?',
      '','## Data gaps / research integrity',
      '- No verified October 30 trading volume, TVL, open interest or realized PnL snapshot was fetched in the current execution environment.',
      '- DefiLlama current *derivatives volume* overview requires an API plan; this project does not use it or claim free access.',
      '- Fees and open interest may be available from separate free endpoints; their methodology and instrument coverage can differ.',
      '- The comparison does NOT endorse or recommend trading any product; it is a public-documentation audit.',
      '','## Reproducibility',
      '`python3 src/build_report.py` regenerates the matrix, Markdown and SVG without external dependencies. For fresh DefiLlama free fees/OI data run `python3 src/fetch_llama.py --live`; live data is not a prerequisite for the qualitative report.',
      '','## References']
    for p in pp:
        lines.append(f'- **{p["name"]}**: '+' · '.join(p['source_urls']))
    return '\n'.join(lines)+'\n'

def build(root:Path):
    data=json.loads((root/'data'/'protocols.json').read_text(encoding='utf-8'));validate(data)
    (root/'artifacts').mkdir(exist_ok=True)
    with (root/'artifacts'/'design_matrix.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,COLUMNS);w.writeheader();w.writerows(rows(data))
    (root/'artifacts'/'comparison.svg').write_text(svg(data),encoding='utf-8')
    (root/'artifacts'/'research_report.md').write_text(report(data),encoding='utf-8')
    return len(data['protocols'])
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a=parser.parse_args()
    print('built',build(a.root),'protocols')
