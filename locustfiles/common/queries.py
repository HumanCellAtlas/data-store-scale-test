query_large_files = {
    "query": {
        "range" : {
            "manifest.files.size" : {
                "gte" : 500000000
            }
        }
    }
}

query_medium_files = {
    "query": {
        "range" : {
            "manifest.files.size" : {
                "gte" : 40000000,
                "lte" : 70000000
            }
        }
    }
}

query_all = {}