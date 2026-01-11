"""
Dune Dashboard Creator - Automatically create and manage Dune Analytics queries and dashboards
"""
import os
from typing import List, Optional
from dotenv import load_dotenv
from dune_client.client import DuneClient
from dune_client.types import QueryParameter

load_dotenv()


class DuneDashboardCreator:
    """Main class for creating and managing Dune Analytics queries and dashboards"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Dune Dashboard Creator

        Args:
            api_key: Dune API key (if not provided, will use DUNE_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("DUNE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "DUNE_API_KEY not found. Please set it in .env file or pass as argument"
            )
        self.client = DuneClient(api_key=self.api_key)

    def create_query(
        self,
        name: str,
        query_sql: str,
        params: Optional[List[QueryParameter]] = None,
        is_private: bool = False,
    ) -> int:
        """
        Create a new query on Dune Analytics

        NOTE: Requires Dune Plus plan or higher

        Args:
            name: Name of the query
            query_sql: SQL query string
            params: Optional list of query parameters
            is_private: Whether the query should be private

        Returns:
            query_id: The ID of the created query
        """
        print(f"Creating query: {name}")

        try:
            query = self.client.create_query(
                name=name,
                query_sql=query_sql,
                params=params or [],
                is_private=is_private,
            )

            query_id = query.base.query_id
            print(f"✓ Successfully created query with ID: {query_id}")
            print(f"  URL: https://dune.com/queries/{query_id}")

            return query_id
        except Exception as e:
            if "403" in str(e) or "Forbidden" in str(e):
                print(f"✗ Error: Query creation requires a Dune Plus plan or higher")
                print(f"  Your current API key doesn't have permission to create queries")
                print(f"  Visit https://dune.com/pricing to upgrade your plan")
                raise
            else:
                raise

    def update_query(
        self,
        query_id: int,
        name: Optional[str] = None,
        query_sql: Optional[str] = None,
        params: Optional[List[QueryParameter]] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ):
        """
        Update an existing query

        Args:
            query_id: ID of the query to update
            name: New name for the query
            query_sql: New SQL query string
            params: New list of query parameters
            description: Query description
            tags: List of tags
        """
        print(f"Updating query {query_id}...")

        self.client.update_query(
            query_id=query_id,
            name=name,
            query_sql=query_sql,
            params=params,
            description=description,
            tags=tags,
        )

        print(f"✓ Successfully updated query {query_id}")

    def execute_query(self, query_id: int, performance: str = "medium"):
        """
        Execute a query and return the results
        This works with all API tiers (including free)

        Args:
            query_id: ID of the query to execute
            performance: Query performance setting (medium, large)

        Returns:
            Query results
        """
        print(f"Executing query {query_id}...")
        results = self.client.run_query(query_id=query_id, performance=performance)
        print(f"✓ Query executed successfully")
        print(f"  Result ID: {results.result_id}")
        return results

    def get_query_result(self, query_id: int):
        """
        Get the latest results for a query without re-running it
        This works with all API tiers (including free)

        Args:
            query_id: ID of the query

        Returns:
            Query results
        """
        print(f"Fetching latest results for query {query_id}...")
        results = self.client.get_latest_result(query_id)
        print(f"✓ Results fetched successfully")
        return results


def demo_existing_queries(query_ids: Optional[List[int]] = None):
    """
    Demo executing existing queries - works with all API tiers including free

    Args:
        query_ids: List of query IDs to execute. If None, shows instructions.
    """
    creator = DuneDashboardCreator()

    print("\nDemo: Executing existing queries (works with free tier)")
    print("="*60)

    if not query_ids:
        print("\n💡 To test with your existing queries:")
        print("   1. Open your dashboard: https://dune.com/madmax112608/beacon-depositor-staking-review")
        print("   2. Click on any visualization to see the query")
        print("   3. Copy the query ID from the URL (e.g., https://dune.com/queries/<ID>)")
        print("   4. Update the query_ids list in demo_existing_queries()")
        print()
        print("   Example:")
        print("   demo_existing_queries([123456, 789012])")
        return

    for query_id in query_ids:
        try:
            print(f"\n📊 Query {query_id}:")
            print(f"   URL: https://dune.com/queries/{query_id}")

            # Fetch latest results without re-running
            results = creator.get_query_result(query_id)

            if hasattr(results, 'get_rows'):
                rows = results.get_rows()
                print(f"   ✓ Retrieved {len(rows)} rows")
                if rows and len(rows) > 0:
                    print(f"   Sample data: {rows[0]}")
            else:
                print(f"   ✓ Results retrieved successfully")

        except Exception as e:
            error_msg = str(e)
            print(f"   ✗ Error: {error_msg}")
            if "404" in error_msg:
                print(f"   (Query not found - check the ID or make sure it's public)")
            elif "403" in error_msg:
                print(f"   (Query is private - you need to own it or it needs to be public)")


def create_example_queries():
    """
    Create example queries for a sample dashboard
    NOTE: Requires Dune Plus plan or higher
    """
    print("\n⚠️  Query creation requires a Dune Plus plan or higher")
    print("   If you don't have Plus, you can still execute existing queries")
    print("   See demo_existing_queries() for examples\n")

    creator = DuneDashboardCreator()

    # Example 1: Ethereum Daily Transactions
    eth_daily_tx = """
    SELECT
        DATE_TRUNC('day', block_time) as date,
        COUNT(*) as transaction_count
    FROM ethereum.transactions
    WHERE block_time >= NOW() - INTERVAL '{{days}}' DAY
    GROUP BY 1
    ORDER BY 1 DESC
    """

    try:
        query1_id = creator.create_query(
            name="Ethereum Daily Transactions (Last N Days)",
            query_sql=eth_daily_tx,
            params=[QueryParameter.number_type(name="days", value=30)],
            is_private=False,
        )

        # Example 2: Top Gas Spenders
        top_gas = """
        SELECT
            "from" as address,
            COUNT(*) as tx_count,
            SUM(gas_used * gas_price) / 1e18 as total_eth_spent
        FROM ethereum.transactions
        WHERE block_time >= NOW() - INTERVAL '7' DAY
        GROUP BY 1
        ORDER BY 3 DESC
        LIMIT {{limit}}
        """

        query2_id = creator.create_query(
            name="Top Gas Spenders (Last 7 Days)",
            query_sql=top_gas,
            params=[QueryParameter.number_type(name="limit", value=100)],
            is_private=False,
        )

        print("\n" + "="*60)
        print("Queries created successfully!")
        print("="*60)
        print("\nNext steps:")
        print("1. Go to https://dune.com/")
        print("2. Click 'New Dashboard'")
        print("3. Add the following queries to your dashboard:")
        print(f"   - Query {query1_id}: https://dune.com/queries/{query1_id}")
        print(f"   - Query {query2_id}: https://dune.com/queries/{query2_id}")
        print("\nYou can customize the visualizations for each query in the dashboard!")

    except Exception:
        print("\n💡 Alternative: Execute existing queries instead")
        print("   Run demo_existing_queries() to see how to work with existing queries")


def main():
    """Main entry point"""
    print("Dune Dashboard Creator")
    print("=" * 60)

    # Check if API key is set
    if not os.getenv("DUNE_API_KEY"):
        print("ERROR: DUNE_API_KEY not found in environment variables")
        print("\nPlease:")
        print("1. Copy .env.example to .env")
        print("2. Add your Dune API key to the .env file")
        print("3. Get your API key from: https://dune.com/settings/api")
        return

    print("\n📖 Choose an option:")
    print("   1. Create new queries (requires Plus plan)")
    print("   2. Execute existing queries (works with free tier)")
    print()

    # Try to create queries (will show helpful error if user doesn't have Plus)
    create_example_queries()

    # Show free tier alternative
    print("\n" + "="*60)
    demo_existing_queries()


if __name__ == "__main__":
    main()
