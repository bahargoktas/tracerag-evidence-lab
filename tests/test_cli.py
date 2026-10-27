import json
from pathlib import Path
from tracerag.cli import main

ROOT = Path(__file__).resolve().parents[1]


def test_check_data(capsys):
    assert main(['--root', str(ROOT), 'check-data']) == 0
    assert json.loads(capsys.readouterr().out)['documents'] == 32


def test_ask_output_is_structured(capsys):
    assert main(['--root', str(ROOT), 'ask', '--query', 'JWKS key rotation']) == 0
    output = json.loads(capsys.readouterr().out)
    assert 'abstained' in output
    assert output['retrieved']
