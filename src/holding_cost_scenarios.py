#!/usr/bin/env python3
"""Generate hypothetical holding-time fee scenarios, NOT verified venue execution prices.

The illustrative penalty decay is an analytical assumption, NOT a reconstruction
of Sai's smart contract. No online execution, historical candles, or live quotes.
"""
from __future__ import annotations
import argparse,csv,math
from pathlib import Path

YEAR_SECONDS=365*24*3600
HORIZONS=[('30 seconds',30),('3 minutes',180),('12 minutes',720),('30 minutes',1800),('1 day',86400)]
ASSUMPTIONS={
    'notional_usd':10000.0,
    'entry_taker_bps':5.0,
    'exit_taker_bps':5.0,
    'hypothetical_max_close_penalty_bps':115.0,
    'assumed_penalty_decay_seconds':720,
    'assumed_slippage_bps':4.0,
    'assumed_borrow_apr_bps':1000.0,
}

def penalty_bps(seconds: int, shape: str, p: dict=ASSUMPTIONS) -> float:
    """A *hypothetical* sensitivity curve, not a claim about any actual contract."""
    if seconds<0:raise ValueError('negative hold duration')
    if shape=='none':return 0.0
    max_penalty=float(p['hypothetical_max_close_penalty_bps'])
    window=float(p['assumed_penalty_decay_seconds'])
    if shape=='linear':return max(0.0,max_penalty*(1-seconds/window))
    if shape=='step':return max_penalty if seconds<window else 0.0
    raise ValueError('Unsupported hypothetical shape')

def cost_bps(seconds:int,shape:str, p:dict=ASSUMPTIONS)->dict:
    components={
        'entry_fee_bps':float(p['entry_taker_bps']),
        'exit_fee_bps':float(p['exit_taker_bps']),
        'assumed_slippage_bps':float(p['assumed_slippage_bps']),
        'hypothetical_close_penalty_bps':penalty_bps(seconds,shape,p),
        'hypothetical_borrow_bps':float(p['assumed_borrow_apr_bps'])*seconds/YEAR_SECONDS,
    }
    components['total_bps']=round(sum(components.values()),6)
    components['total_usd']=round(components['total_bps']*float(p['notional_usd'])/10000,4)
    return components

def build_csv(path:Path):
    path.parent.mkdir(parents=True,exist_ok=True)
    rows=[]
    for shape in ('none','linear','step'):
        for label,seconds in HORIZONS:
            rows.append({'curve_is_hypothetical':True,'shape':shape,'hold_label':label,'hold_seconds':seconds,**cost_bps(seconds,shape)})
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    return rows

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path(__file__).resolve().parents[1]/'artifacts'/'illustrative_cost_sensitivity.csv');args=ap.parse_args()
    scenarios=build_csv(args.output)
    print('generated',len(scenarios),'synthetic hypothetical scenarios:',args.output)
    print('WARNING: Not observed fees, not an official Sai fee emulator, not trading advice.')
