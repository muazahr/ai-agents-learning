from app_framework.evaluation import evaluate_router


def test_router_evaluation_cases_pass():
    report = evaluate_router()
    assert report["total"] >= 4
    assert report["failed"] == 0
    assert report["accuracy"] == 1.0


def test_router_evaluation_accepts_custom_cases():
    report = evaluate_router([
        {"name": "weather", "input": "tiempo en Granada", "expected": "weather"},
    ])
    assert report["passed"] == 1
