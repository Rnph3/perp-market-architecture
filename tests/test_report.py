import sys,json,tempfile,unittest,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from build_report import build,validate,report,svg
from fetch_llama import extract,ENDPOINTS
class ResearchKitTests(unittest.TestCase):
    def test_source_evidence_and_unique_protocols(self):
        d=json.loads((ROOT/'data'/'protocols.json').read_text(encoding='utf-8'))
        validate(d);self.assertEqual(len(d['protocols']),4)
    def test_build_is_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp);(tmp/'data').mkdir();(tmp/'data'/'protocols.json').write_bytes((ROOT/'data'/'protocols.json').read_bytes())
            self.assertEqual(build(tmp),4)
            with (tmp/'artifacts'/'design_matrix.csv').open(encoding='utf-8',newline='') as source:
                rows=list(csv.DictReader(source))
            self.assertEqual([r['name'] for r in rows],['Sai','Hyperliquid','GMX','dYdX Chain'])
            self.assertIn('Falsifiable follow-up questions',(tmp/'artifacts'/'research_report.md').read_text())
            self.assertIn('<svg',(tmp/'artifacts'/'comparison.svg').read_text())
    def test_no_fake_perp_derivatives_volume_endpoint(self):
        self.assertNotIn('derivatives',str(ENDPOINTS))
    def test_extract_missing_metrics_not_zero(self):
        p={'protocols':[{'name':'Hyperliquid','total24h':None},{'name':'Unrelated','total24h':99}]}
        r=extract(p);self.assertEqual(len(r),1);self.assertIsNone(r[0]['total24h'])
if __name__=='__main__':unittest.main()
