"""Parancssori belépési pont az A* összehasonlító kísérletekhez."""

from pathlib import Path

from .experiments import run_scenario_comparison, write_results


if __name__ == "__main__":
    output = (
        Path(__file__).resolve().parent
        / "results"
        / "tables"
        / "heuristic_comparison.csv"
    )
    rows = run_scenario_comparison()
    write_results(rows, output)
    print(f"{len(rows)} eredmény mentve: {output}")
