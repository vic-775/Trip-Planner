from tools.tavily import tavily_search
from tools.flight import search_flights

# test tavily_search tool
# res = tavily_search("best hotels in Diani beach, Kenya")
# print(res)

# test search_flights tool
def test_search_flights():
    result = search_flights(
        origin="NBO",
        destination="NRT",
        limit=5,
    )

    print(result)


if __name__ == "__main__":
    test_search_flights()