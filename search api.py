def search_serpapi(query):
    """
    Perform a web search using SerpAPI.
    """
    api_key = " "  #replace this with your search api key
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
    }
    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code == 200:
        return response.json().get("organic_results", [])
    else:
        return []
