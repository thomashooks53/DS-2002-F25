#!/usr/bin/env python3
import sys
from update_portfolio import main as etl_main
from generate_summary import main as report_main


def run_production_pipeline() -> None:
    print("Starting production pipeline...", file=sys.stderr)
    print("ETL Step: running update_portfolio...", file=sys.stderr)
    etl_main()
    print("ETL Step complete.", file=sys.stderr)

    print("Reporting Step: running generate_summary...", file=sys.stderr)
    report_main()
    print("Production pipeline completed.", file=sys.stderr)


if __name__ == "__main__":
    run_production_pipeline()