from neo4j_client import Neo4jGraphEngine


graph = Neo4jGraphEngine()


try:

    print(
        "\nChecking Neo4j connection..."
    )

    graph.verify_connection()


    print(
        "\nCreating advanced mule network..."
    )


    # =================================================
    # VICTIMS → PRIMARY MULE
    # =================================================

    graph.add_transaction(
        "VICTIM101",
        "MULE100",
        15000
    )


    graph.add_transaction(
        "VICTIM102",
        "MULE100",
        12000
    )


    graph.add_transaction(
        "VICTIM103",
        "MULE100",
        18000
    )


    # =================================================
    # LEVEL 1
    # =================================================

    graph.add_transaction(
        "MULE100",
        "MULE200",
        12000
    )


    graph.add_transaction(
        "MULE100",
        "MULE201",
        10000
    )


    graph.add_transaction(
        "MULE100",
        "MULE202",
        9000
    )


    # =================================================
    # LEVEL 2
    # =================================================

    graph.add_transaction(
        "MULE200",
        "MULE300",
        9000
    )


    graph.add_transaction(
        "MULE201",
        "MULE301",
        8000
    )


    graph.add_transaction(
        "MULE202",
        "MULE302",
        7000
    )


    # =================================================
    # LEVEL 3
    # =================================================

    graph.add_transaction(
        "MULE300",
        "EXIT001",
        7000
    )


    graph.add_transaction(
        "MULE301",
        "EXIT002",
        6000
    )


    print(
        "\nAnalyzing MULE100..."
    )


    result = graph.analyze_account(
        "MULE100"
    )


    print(
        "\n===================================="
    )

    print(
        "   ADVANCED GRAPH FRAUD ANALYSIS"
    )

    print(
        "===================================="
    )


    print(
        "\nAccount:",
        result["account_id"]
    )


    print(
        "Graph Risk Score:",
        result["graph_risk_score"]
    )


    print(
        "Graph Risk Level:",
        result["graph_risk_level"]
    )


    print(
        "\n--- Direct Activity ---"
    )


    print(
        "Incoming:",
        result["incoming_transactions"]
    )


    print(
        "Unique Senders:",
        result["unique_senders"]
    )


    print(
        "Outgoing:",
        result["outgoing_transactions"]
    )


    print(
        "Unique Receivers:",
        result["unique_receivers"]
    )


    print(
        "\n--- Velocity ---"
    )


    print(
        "Total Transactions:",
        result["total_transactions"]
    )


    print(
        "Pass Through Ratio:",
        result["pass_through_ratio"]
    )


    print(
        "\n--- Multi-Hop Network ---"
    )


    print(
        "Multi-Hop Paths:",
        result["multi_hop_paths"]
    )


    print(
        "Reachable Accounts:",
        result["reachable_accounts"]
    )


    print(
        "Maximum Hop Depth:",
        result["max_hop_depth"]
    )


    print(
        "Rapid Chains:",
        result["rapid_chain_count"]
    )


    print(
        "\n--- Risk Reasons ---"
    )


    for reason in result["reasons"]:

        print(
            "•",
            reason
        )


    print(
        "\n--- Decision ---"
    )


    if (
        result["graph_risk_level"]
        == "HIGH"
    ):

        print(
            "🚨 ADVANCED MULE NETWORK DETECTED"
        )


    elif (
        result["graph_risk_level"]
        == "MEDIUM"
    ):

        print(
            "⚠️ SUSPICIOUS TRANSACTION NETWORK"
        )


    else:

        print(
            "✅ LOW GRAPH RISK"
        )


finally:

    graph.close()