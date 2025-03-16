import requests
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Project
mcp = FastMCP("github_project", dependencies=["requests"])

BASE_URL = "https://api.github.com"

# Use a session for optimized performance
session = requests.Session()

def make_request(endpoint: str):
    """
    Helper function to make GET requests to the GitHub API with error handling.
    """
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "FastMCP-GitHub-Client"
    }

    try:
        response = session.get(url, headers=headers, timeout=5)
        response.raise_for_status()  # Raise an error for HTTP failures

        # Handle rate-limiting
        if response.status_code == 403 and "X-RateLimit-Remaining" in response.headers:
            return {"error": "GitHub API rate limit exceeded. Try again later."}

        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Check your internet connection."}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def clean_user_data(data):
    """ Keep only important user fields. """
    if "error" in data:
        return data
    return {
        "username": data.get("login"),
        "id": data.get("id"),
        "followers": data.get("followers"),
        "repos": data.get("public_repos"),
        "bio": data.get("bio") or "No bio",
    }

def clean_repo_data(data):
    """ Keep only important repository fields. """
    if "error" in data:
        return data
    return {
        "name": data.get("name"),
        "owner": data["owner"]["login"] if "owner" in data else None,
        "stars": data.get("stargazers_count"),
        "forks": data.get("forks_count"),
        "language": data.get("language") or "Unknown",
    }

@mcp.tool()
def search_users(username: str):
    """
    Search for GitHub users (returns minimal data).
    Args:
      username: name of the github profile to be searched
    
    return:
        list of the data from the git hub api
    """
    data = make_request(f"/search/users?q={username}&per_page=5")
    return [{"username": user["login"], "id": user["id"]} for user in data.get("items", [])]

@mcp.tool()
def get_user_details(username: str):
    """
    Fetch details of a GitHub user (returns minimal data).

    Args:
      username: name of the github profile to be searched
    
    return:
        list of the data from the git hub api
    """
    return clean_user_data(make_request(f"/users/{username}"))

@mcp.tool()
def search_repositories(repo_name: str):
    """
    Search for repositories on GitHub (returns minimal data).
    Args:
      repo_name: name of the github repository to be searched
    
    return:
        list of the data from the git hub api
    """
    data = make_request(f"/search/repositories?q={repo_name}&per_page=5")
    return [clean_repo_data(repo) for repo in data.get("items", [])]

@mcp.tool()
def get_repository_details(owner: str, repo: str):
    """
    Get details of a GitHub repository (returns minimal data).
    Args:
      owner: name of the github repository owner to be searched
    
    return:
        Dictonary of the data from the git hub api
    """
    return clean_repo_data(make_request(f"/repos/{owner}/{repo}"))

@mcp.tool()
def get_user_repos(username: str):
    """
    Fetch public repositories of a user (returns minimal data).
    Args:
      username: name of the github profile to be searched
    
    return:
        list of the data from the git hub api
    """
    data = make_request(f"/users/{username}/repos?per_page=5")
    return [clean_repo_data(repo) for repo in data]

@mcp.prompt()
def github_user_summary(username: str):
    """
    Generate a structured summary of a GitHub user including user details and top repositories.
    
    Args:
      username: name of the github profile to be searched
    
    return:
        list of the data from the git hub api
    """
    return {
        "user_info": get_user_details(username),
        "top_repositories": get_user_repos(username)
    }

# Example Usage (Uncomment to Test)
# print(search_users("torvalds"))
# print(get_user_details("torvalds"))
# print(search_repositories("fastapi"))
# print(get_repository_details("tiangolo", "fastapi"))
# print(get_user_repos("torvalds"))
# print(github_user_summary("torvalds"))
