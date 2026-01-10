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

        Args:
            name: Name of the query
            query_sql: SQL query string
            params: Optional list of query parameters
            is_private: Whether the query should be private

        Returns:
            query_id: The ID of the created query
        """
        print(f"Creating query: {name}")

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

    def execute_query(self, query_id: int) -> dict:
        """
        Execute a query and return the results

        Args:
            query_id: ID of the query to execute

        Returns:
            Query results as a dictionary
        """
        print(f"Executing query {query_id}...")
        results = self.client.get_latest_result(query_id)
        print(f"✓ Query executed successfully")
        return results


def create_example_queries():
    """Create example queries for a sample dashboard"""
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

    # Create example queries
    create_example_queries()


if __name__ == "__main__":
    main()
