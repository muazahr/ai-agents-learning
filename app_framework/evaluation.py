"""Pequeñas evaluaciones deterministas para comprobar piezas del proyecto sin API."""

from app_framework.agent_multiagent import route_request

EVALUATION_CASES = [
    {"name": "detecta matemáticas", "input": "¿Cuánto es 12 * 4?", "expected": "math"},
    {"name": "detecta meteorología", "input": "¿Qué tiempo hace en Granada?", "expected": "weather"},
    {"name": "detecta fecha", "input": "¿Qué hora es ahora?", "expected": "datetime"},
    {"name": "detecta investigación", "input": "Investiga la historia de Roma", "expected": "research"},
]


def evaluate_router(cases=None) -> dict:
    """Ejecuta casos conocidos contra el router y devuelve métricas reproducibles."""
    cases = EVALUATION_CASES if cases is None else cases
    results = []
    for case in cases:
        actual = route_request(case["input"])
        passed = case["expected"] in actual
        results.append({
            "name": case["name"],
            "passed": passed,
            "expected": case["expected"],
            "actual": actual,
        })
    total = len(results)
    passed_count = sum(item["passed"] for item in results)
    return {
        "total": total,
        "passed": passed_count,
        "failed": total - passed_count,
        "accuracy": passed_count / total if total else 1.0,
        "results": results,
    }


def main() -> int:
    """Muestra un informe legible y devuelve un código de salida útil para CI."""
    report = evaluate_router()
    print("Evaluación local del router")
    print("===========================")
    for item in report["results"]:
        status = "OK" if item["passed"] else "FALLO"
        print("[{}] {} | esperado={} | obtenido={}".format(
            status, item["name"], item["expected"], item["actual"]
        ))
    print("\nResultado: {}/{} correctos ({:.0%})".format(
        report["passed"], report["total"], report["accuracy"]
    ))
    return 0 if report["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
