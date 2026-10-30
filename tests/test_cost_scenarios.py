import sys,unittest,tempfile,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from holding_cost_scenarios import penalty_bps,cost_bps,build_csv
class CostSensitivityTests(unittest.TestCase):
    def test_hypothetical_curve_nonnegative_monotone(self):
        vals=[penalty_bps(s,'linear') for s in [0,30,180,720,3600]]
        self.assertEqual(vals[-1],0)
        self.assertEqual(vals,sorted(vals,reverse=True))
    def test_no_actual_market_observations(self):
        r=cost_bps(30,'none')
        self.assertAlmostEqual(r['hypothetical_close_penalty_bps'],0)
        self.assertGreater(r['total_bps'],0)
    def test_export_is_labeled_hypothetical(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'demo.csv';build_csv(p)
            with p.open(encoding='utf-8') as f:rows=list(csv.DictReader(f))
            self.assertEqual(len(rows),15)
            self.assertTrue(all(x['curve_is_hypothetical']=='True' for x in rows))
if __name__=='__main__':unittest.main()
