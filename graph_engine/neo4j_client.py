import os
import time
import uuid

import truststore

truststore.inject_into_ssl()

from dotenv import load_dotenv
from neo4j import GraphDatabase


# =====================================================
# ENVIRONMENT
# =====================================================

load_dotenv(
    override=True
)


NEO4J_URI = os.getenv(
    "NEO4J_URI"
)

NEO4J_USERNAME = os.getenv(
    "NEO4J_USERNAME"
)

NEO4J_PASSWORD = os.getenv(
    "NEO4J_PASSWORD"
)


# =====================================================
# GRAPH ENGINE
# =====================================================

class Neo4jGraphEngine:

    def __init__(self):

        if not NEO4J_URI:
            raise ValueError(
                "NEO4J_URI missing from .env"
            )

        if not NEO4J_USERNAME:
            raise ValueError(
                "NEO4J_USERNAME missing from .env"
            )

        if not NEO4J_PASSWORD:
            raise ValueError(
                "NEO4J_PASSWORD missing from .env"
            )


        self.driver = GraphDatabase.driver(

            NEO4J_URI,

            auth=(
                NEO4J_USERNAME,
                NEO4J_PASSWORD
            )
        )


    # =================================================
    # CONNECTION TEST
    # =================================================

    def verify_connection(self):

        self.driver.verify_connectivity()

        print(
            "Neo4j connection successful!"
        )


    # =================================================
    # ADD TRANSACTION
    # =================================================

    def add_transaction(
        self,
        sender,
        receiver,
        amount,
        transaction_id=None
    ):

        sender = (
            sender
            .strip()
            .upper()
        )

        receiver = (
            receiver
            .strip()
            .upper()
        )


        if transaction_id is None:

            transaction_id = str(
                uuid.uuid4()
            )


        timestamp_ms = int(
            time.time() * 1000
        )


        query = """

        MERGE (
            sender:Account {
                account_id: $sender
            }
        )

        MERGE (
            receiver:Account {
                account_id: $receiver
            }
        )

        CREATE (
            sender
        )-[
            tx:TRANSFERRED_TO
        ]->(
            receiver
        )

        SET
            tx.transaction_id =
                $transaction_id,

            tx.amount =
                $amount,

            tx.timestamp_ms =
                $timestamp_ms


        RETURN

            sender.account_id
                AS sender,

            receiver.account_id
                AS receiver,

            tx.transaction_id
                AS transaction_id

        """


        with self.driver.session() as session:

            result = session.run(

                query,

                sender=sender,

                receiver=receiver,

                amount=float(amount),

                transaction_id=
                    transaction_id,

                timestamp_ms=
                    timestamp_ms
            )


            record = result.single()


        return {

            "sender":
                record["sender"],

            "receiver":
                record["receiver"],

            "transaction_id":
                record[
                    "transaction_id"
                ]
        }


    # =================================================
    # ADVANCED ACCOUNT ANALYSIS
    # =================================================

    def analyze_account(
        self,
        account_id,
        window_minutes=10
    ):

        account_id = (
            account_id
            .strip()
            .upper()
        )


        window_ms = (
            window_minutes
            * 60
            * 1000
        )


        # =================================================
        # 1. INCOMING ACTIVITY
        # =================================================

        incoming_query = """

        MATCH
        (sender:Account)
        -[tx:TRANSFERRED_TO]->
        (account:Account {
            account_id: $account_id
        })

        WHERE
            tx.timestamp_ms >=
            timestamp() - $window_ms


        RETURN

            count(tx)
                AS incoming_transactions,

            count(
                DISTINCT sender
            )
                AS unique_senders,

            coalesce(
                sum(tx.amount),
                0
            )
                AS incoming_amount

        """


        # =================================================
        # 2. OUTGOING ACTIVITY
        # =================================================

        outgoing_query = """

        MATCH
        (account:Account {
            account_id: $account_id
        })
        -[tx:TRANSFERRED_TO]->
        (receiver:Account)

        WHERE
            tx.timestamp_ms >=
            timestamp() - $window_ms


        RETURN

            count(tx)
                AS outgoing_transactions,

            count(
                DISTINCT receiver
            )
                AS unique_receivers,

            coalesce(
                sum(tx.amount),
                0
            )
                AS outgoing_amount

        """


        # =================================================
        # 3. MULTI-HOP NETWORK
        # =================================================

        multi_hop_query = """

        MATCH p =
        (
            account:Account {
                account_id: $account_id
            }
        )
        -[
            relationships:
            TRANSFERRED_TO*1..3
        ]->
        (
            target:Account
        )

        WHERE

            all(
                r IN relationships

                WHERE

                    r.timestamp_ms >=
                    timestamp() - $window_ms
            )


        RETURN

            count(p)
                AS path_count,

            count(
                DISTINCT target
            )
                AS reachable_accounts,

            coalesce(
                max(
                    length(p)
                ),
                0
            )
                AS max_hop_depth

        """


        # =================================================
        # 4. RAPID 2–3 HOP CHAINS
        # =================================================

        rapid_chain_query = """

        MATCH p =
        (
            account:Account {
                account_id: $account_id
            }
        )
        -[
            relationships:
            TRANSFERRED_TO*2..3
        ]->
        (
            target:Account
        )

        WHERE

            all(
                r IN relationships

                WHERE

                    r.timestamp_ms >=
                    timestamp() - $window_ms
            )

            AND

            (
                reduce(
                    latest = 0,

                    r IN relationships |

                    CASE
                        WHEN r.timestamp_ms > latest
                        THEN r.timestamp_ms
                        ELSE latest
                    END
                )

                -

                reduce(
                    earliest = 9999999999999,

                    r IN relationships |

                    CASE
                        WHEN r.timestamp_ms < earliest
                        THEN r.timestamp_ms
                        ELSE earliest
                    END
                )

            ) <= 300000


        RETURN

            count(p)
                AS rapid_chain_count

        """


        # =================================================
        # EXECUTE QUERIES
        # =================================================

        with self.driver.session() as session:

            incoming = (
                session.run(

                    incoming_query,

                    account_id=
                        account_id,

                    window_ms=
                        window_ms
                )
                .single()
            )


            outgoing = (
                session.run(

                    outgoing_query,

                    account_id=
                        account_id,

                    window_ms=
                        window_ms
                )
                .single()
            )


            multi_hop = (
                session.run(

                    multi_hop_query,

                    account_id=
                        account_id,

                    window_ms=
                        window_ms
                )
                .single()
            )


            rapid_chain = (
                session.run(

                    rapid_chain_query,

                    account_id=
                        account_id,

                    window_ms=
                        window_ms
                )
                .single()
            )


        # =================================================
        # EXTRACT VALUES
        # =================================================

        incoming_transactions = int(
            incoming[
                "incoming_transactions"
            ]
        )


        unique_senders = int(
            incoming[
                "unique_senders"
            ]
        )


        incoming_amount = float(
            incoming[
                "incoming_amount"
            ]
        )


        outgoing_transactions = int(
            outgoing[
                "outgoing_transactions"
            ]
        )


        unique_receivers = int(
            outgoing[
                "unique_receivers"
            ]
        )


        outgoing_amount = float(
            outgoing[
                "outgoing_amount"
            ]
        )


        multi_hop_paths = int(
            multi_hop[
                "path_count"
            ]
        )


        reachable_accounts = int(
            multi_hop[
                "reachable_accounts"
            ]
        )


        max_hop_depth = int(
            multi_hop[
                "max_hop_depth"
            ]
        )


        rapid_chain_count = int(
            rapid_chain[
                "rapid_chain_count"
            ]
        )


        total_transactions = (

            incoming_transactions
            +
            outgoing_transactions
        )


        # =================================================
        # PASS-THROUGH RATIO
        # =================================================

        if incoming_amount > 0:

            pass_through_ratio = (

                outgoing_amount
                /
                incoming_amount
            )

        else:

            pass_through_ratio = 0.0


        pass_through_ratio = round(
            pass_through_ratio,
            2
        )


        # =================================================
        # GRAPH RISK SCORE
        # =================================================

        graph_risk_score = 0

        reasons = []


        # ---------------------------------------------
        # Many unique senders
        # ---------------------------------------------

        if unique_senders >= 3:

            graph_risk_score += 15

            reasons.append(
                "Multiple unique senders detected"
            )


        # ---------------------------------------------
        # Fan-out
        # ---------------------------------------------

        if unique_receivers >= 3:

            graph_risk_score += 20

            reasons.append(
                "Funds distributed to multiple accounts"
            )


        # ---------------------------------------------
        # High velocity
        # ---------------------------------------------

        if total_transactions >= 5:

            graph_risk_score += 20

            reasons.append(
                "High transaction velocity detected"
            )


        # ---------------------------------------------
        # Pass-through
        # ---------------------------------------------

        if (
            incoming_amount > 0
            and
            outgoing_amount > 0
            and
            pass_through_ratio >= 0.70
        ):

            graph_risk_score += 15

            reasons.append(
                "High rapid pass-through ratio detected"
            )


        # ---------------------------------------------
        # Multi-hop spread
        # ---------------------------------------------

        if reachable_accounts >= 4:

            graph_risk_score += 15

            reasons.append(
                "Funds spread across a multi-hop network"
            )


        # ---------------------------------------------
        # Deep chain
        # ---------------------------------------------

        if max_hop_depth >= 3:

            graph_risk_score += 10

            reasons.append(
                "Three-hop transaction chain detected"
            )


        # ---------------------------------------------
        # Rapid laundering-like chain
        # ---------------------------------------------

        if rapid_chain_count >= 1:

            graph_risk_score += 20

            reasons.append(
                "Rapid 2-3 hop fund movement detected"
            )


        graph_risk_score = min(
            graph_risk_score,
            100
        )


        # =================================================
        # GRAPH RISK LEVEL
        # =================================================

        if graph_risk_score >= 70:

            graph_risk_level = "HIGH"


        elif graph_risk_score >= 40:

            graph_risk_level = "MEDIUM"


        else:

            graph_risk_level = "LOW"


        # =================================================
        # RETURN
        # =================================================

        return {

            "account_id":
                account_id,


            "graph_risk_score":
                graph_risk_score,


            "graph_risk_level":
                graph_risk_level,


            "incoming_transactions":
                incoming_transactions,


            "unique_senders":
                unique_senders,


            "incoming_amount":
                incoming_amount,


            "outgoing_transactions":
                outgoing_transactions,


            "unique_receivers":
                unique_receivers,


            "outgoing_amount":
                outgoing_amount,


            "total_transactions":
                total_transactions,


            "pass_through_ratio":
                pass_through_ratio,


            "multi_hop_paths":
                multi_hop_paths,


            "reachable_accounts":
                reachable_accounts,


            "max_hop_depth":
                max_hop_depth,


            "rapid_chain_count":
                rapid_chain_count,


            "reasons":
                reasons
        }


    # =================================================
    # CLOSE
    # =================================================

    def close(self):

        self.driver.close()