# Dune Dashboard Creator

Automatically create and manage Dune Analytics queries and dashboards using Python and the official Dune API.

## Existing Dashboards

Dashboards with insights into crypto trading:
1. [Beacon Depositor Review](https://dune.com/madmax112608/beacon-depositor-staking-review)
2. [Uniswap V2 vs V3](https://dune.com/madmax112608/uniswap-v2-vs-v3)

## Features

- Create Dune Analytics queries programmatically using Python
- Update and manage existing queries
- Execute queries and retrieve results as pandas DataFrames
- Display results in clean, formatted tables
- Export query results to CSV files
- Interactive CLI with user-friendly prompts
- Built with the official `dune-client` library
- Easy setup with `uv` package manager

## Prerequisites

- Python 3.13+
- A Dune Analytics account
- Dune API key (get it from [https://dune.com/settings/api](https://dune.com/settings/api))

## Important: API Plan Requirements

**Query Creation** (create_query, update_query) requires:
- **Dune Plus plan or higher**
- Free tier API keys will receive a 403 Forbidden error when attempting to create/update queries

**Query Execution** (execute_query, get_query_result) works with:
- **All API tiers including free**
- You can execute and retrieve results from existing public queries

If you have a free tier API key, you can still use this tool to:
- Execute existing queries
- Fetch query results
- Integrate Dune data into your applications

To create queries programmatically, visit [https://dune.com/pricing](https://dune.com/pricing) to upgrade to Plus.

## Setup

1. Clone this repository:
```bash
git clone <your-repo-url>
cd dunedashboards
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Set up your environment variables:
```bash
cp .env.example .env
```

4. Add your Dune API key to the `.env` file:
```
DUNE_API_KEY=your_api_key_here
```

## Usage

### Running the Interactive Tool

The repository includes an interactive CLI tool:

```bash
uv run main.py
```

You'll see an interactive menu with three options:
1. **Create new queries** (requires Plus plan) - Creates example queries for a dashboard
2. **Execute existing queries** (works with free tier) - Fetches results from your existing queries
3. **Exit** - Quit the program

#### Option 2: Execute Existing Queries

When you select option 2, you'll be prompted to enter query IDs:
- Enter one or more query IDs separated by commas (e.g., `123456,789012`)
- The tool will fetch and display results for each query
- Works with any public query or your own private queries

**Example session:**
```
Enter your choice (1-3): 2

Enter query IDs (comma-separated, e.g., 123456,789012): 6499277

📊 Query 6499277:
   URL: https://dune.com/queries/6499277
Fetching latest results for query 6499277...
✓ Results fetched successfully
   ✓ Retrieved 6 rows

   Data Preview (first 10 rows):
--------------------------------------------------------------------------------
 brier_score  cumulative_avg_brier_score        day                 market  outcome predicted_probability
      0.2025                    0.098050 2025-01-10  Fed Rate Hike Q1 2025        0                  0.45
      0.0625                    0.098050 2025-01-10   Will BTC reach $100k        1                  0.75
      0.0324                    0.080825 2025-01-09         S&P 500 > 6000        1                  0.82
      0.0784                    0.080825 2025-01-09   Will BTC reach $100k        1                  0.72
      0.1225                    0.106250 2025-01-08 Crypto Regulation Pass        0                  0.35
      0.0900                    0.106250 2025-01-08   Will BTC reach $100k        1                  0.70
--------------------------------------------------------------------------------

   Shape: 6 rows × 6 columns
   Columns: brier_score, cumulative_avg_brier_score, day, market, outcome, predicted_probability

   Save to CSV? (y/n): y
   ✓ Saved to query_6499277_results.csv
```

### Working with Existing Queries (Free Tier Compatible)

You can execute and retrieve results from any public Dune query:

```python
from main import DuneDashboardCreator
import pandas as pd

creator = DuneDashboardCreator()

# Get results from an existing query
query_id = 123456  # Replace with your query ID
results = creator.get_query_result(query_id)

# Convert to pandas DataFrame
rows = results.get_rows()
df = pd.DataFrame(rows)

# Now you can work with the DataFrame
print(df.head())
print(f"Shape: {df.shape}")

# Export to CSV
df.to_csv(f"query_{query_id}_results.csv", index=False)

# Or execute a query (re-run it)
results = creator.execute_query(query_id)
```

To find query IDs:
1. Open any Dune dashboard
2. Click on a visualization
3. The query ID is in the URL: `https://dune.com/queries/<ID>`

### Creating Custom Queries (Plus Plan Required)

**Note:** Creating queries programmatically requires a Dune Plus plan or higher.

You can use the `DuneDashboardCreator` class to create your own queries:

```python
from main import DuneDashboardCreator
from dune_client.types import QueryParameter

creator = DuneDashboardCreator()

# Create a query
query_id = creator.create_query(
    name="My Custom Query",
    query_sql="""
        SELECT
            block_time,
            COUNT(*) as tx_count
        FROM ethereum.transactions
        WHERE block_time >= NOW() - INTERVAL '{{days}}' DAY
        GROUP BY 1
        ORDER BY 1 DESC
    """,
    params=[QueryParameter.number_type(name="days", value=7)],
    is_private=False
)

print(f"Query created: https://dune.com/queries/{query_id}")
```

### Updating Queries

```python
creator.update_query(
    query_id=12345,
    name="Updated Query Name",
    description="New description",
    tags=["ethereum", "transactions"]
)
```

### Executing Queries

```python
results = creator.execute_query(query_id=12345)
print(results)
```

## Creating a Dashboard

After creating queries with this tool:

1. Go to [https://dune.com/](https://dune.com/)
2. Click "New Dashboard"
3. Add your queries to the dashboard using the query IDs
4. Customize visualizations (charts, tables, etc.)
5. Publish your dashboard

## Project Structure

```
dunedashboards/
├── main.py              # Main script with DuneDashboardCreator class
├── pyproject.toml       # Project dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## API Reference

### DuneDashboardCreator

Main class for interacting with Dune Analytics API.

#### Methods

- `create_query(name, query_sql, params=None, is_private=False)` - Create a new query
- `update_query(query_id, name=None, query_sql=None, params=None, description=None, tags=None)` - Update an existing query
- `execute_query(query_id)` - Execute a query and get results

## Resources

- [Dune Analytics Documentation](https://docs.dune.com/home)
- [Dune API Reference](https://docs.dune.com/api-reference/overview/introduction)
- [dune-client GitHub](https://github.com/duneanalytics/dune-client)
- [Query Management Examples](https://docs.dune.com/api-reference/quickstart/queries-eg)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License