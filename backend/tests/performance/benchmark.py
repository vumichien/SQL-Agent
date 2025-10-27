"""
Performance Benchmarking Script

Tests response time performance.
Target: <5s p95
"""

import time
import statistics
import json
from pathlib import Path
from src.detomo_vanna import DetomoVanna


def benchmark_query_time():
    """Benchmark SQL generation response times"""
    print("=" * 80)
    print("PERFORMANCE BENCHMARK")
    print("=" * 80)
    print()

    # Initialize Vanna
    print("Initializing DetomoVanna...")
    vn = DetomoVanna(config={
        "path": "./detomo_vectordb",
        "agent_endpoint": "http://localhost:8000/generate"
    })
    vn.connect_to_sqlite("data/chinook.db")
    print("✓ Connected to database")
    print()

    # Test queries with different complexity levels
    test_queries = [
        # Simple queries
        "How many customers?",
        "How many tracks?",
        "How many albums?",

        # Medium complexity
        "Show top 10 customers by spending",
        "What is the total revenue?",
        "List all albums by AC/DC",
        "How many albums does each artist have?",

        # Complex queries
        "Show revenue by country",
        "Which genre has the most tracks?",
        "List the top 5 customers by total spending",
        "Show the total sales for each employee",

        # Date/filter queries
        "List all tracks longer than 5 minutes",
        "How many invoices were created in 2013?",

        # Japanese queries
        "顧客は何人いますか？",
        "最も売上が高い国はどこですか？"
    ]

    print(f"Running {len(test_queries)} benchmark queries...")
    print()

    # Run benchmarks
    times = []
    results = []

    for i, question in enumerate(test_queries, 1):
        print(f"[{i}/{len(test_queries)}] {question}")

        try:
            start_time = time.time()
            sql = vn.generate_sql(question)
            elapsed = time.time() - start_time

            times.append(elapsed)
            results.append({
                'question': question,
                'sql': sql,
                'response_time': elapsed,
                'success': True
            })

            print(f"    Time: {elapsed:.2f}s")
            print(f"    SQL: {sql[:80]}...")
            print()

        except Exception as e:
            print(f"    ERROR: {str(e)}")
            print()
            results.append({
                'question': question,
                'error': str(e),
                'success': False
            })

    # Calculate statistics
    if not times:
        print("✗ No successful queries to benchmark!")
        return False

    avg_time = statistics.mean(times)
    median_time = statistics.median(times)
    min_time = min(times)
    max_time = max(times)

    # Calculate percentiles
    sorted_times = sorted(times)
    p50 = sorted_times[int(len(sorted_times) * 0.50)]
    p95 = sorted_times[int(len(sorted_times) * 0.95)]
    p99 = sorted_times[int(len(sorted_times) * 0.99)] if len(sorted_times) > 1 else sorted_times[-1]

    # Print results
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()
    print(f"Total queries: {len(test_queries)}")
    print(f"Successful: {len(times)}")
    print(f"Failed: {len(test_queries) - len(times)}")
    print()
    print("Response Time Statistics:")
    print(f"  Min:     {min_time:.2f}s")
    print(f"  Max:     {max_time:.2f}s")
    print(f"  Mean:    {avg_time:.2f}s")
    print(f"  Median:  {median_time:.2f}s")
    print(f"  P50:     {p50:.2f}s")
    print(f"  P95:     {p95:.2f}s")
    print(f"  P99:     {p99:.2f}s")
    print()

    # Check target
    target_p95 = 5.0
    if p95 < target_p95:
        print(f"✓ Target P95 met ({p95:.2f}s < {target_p95}s)")
    else:
        print(f"✗ Target P95 NOT met ({p95:.2f}s ≥ {target_p95}s)")

    print("=" * 80)

    # Save results
    results_file = Path(__file__).parent / 'benchmark_results.json'
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'total_queries': len(test_queries),
                'successful': len(times),
                'failed': len(test_queries) - len(times),
                'min_time': min_time,
                'max_time': max_time,
                'avg_time': avg_time,
                'median_time': median_time,
                'p50': p50,
                'p95': p95,
                'p99': p99,
                'target_p95': target_p95,
                'target_met': p95 < target_p95
            },
            'results': results
        }, f, indent=2, ensure_ascii=False)

    print(f"\nDetailed results saved to: {results_file}")

    return p95 < target_p95


if __name__ == "__main__":
    success = benchmark_query_time()
    exit(0 if success else 1)
