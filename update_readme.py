import os
import re
import requests

USERNAME = "hariomphulre"
TOKEN = os.environ.get("GH_TOKEN")

# --- CONFIGURATION ---
# ONLY PRs from these specific repositories will be shown.
# Format must be "owner/repository-name"
TARGET_REPOS = [
    "facebook/react",               # Example: replace with actual target repos
    "torvalds/linux", 
    "some-org/some-awesome-repo",
    "archlinux/archinstall",
    "nlohmann/json",
]

# How many top PRs to show permanently (the rest go inside the collapsible section)
TOP_COUNT = 5
# ---------------------

if not TOKEN:
    raise ValueError("GH_TOKEN environment variable is not set.")

headers = {"Authorization": f"Bearer {TOKEN}"}

# Fetching a larger batch (100) to ensure we find your target repo PRs
query = """
query {
  user(login: "%s") {
    pullRequests(states: MERGED, first: 100, orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        title
        url
        repository {
          nameWithOwner
          stargazerCount
          forkCount
        }
        comments {
          totalCount
        }
      }
    }
  }
}
""" % USERNAME

def fetch_prs():
    response = requests.post("https://api.github.com/graphql", json={"query": query}, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]["user"]["pullRequests"]["nodes"]
    else:
        raise Exception(f"API request failed: {response.text}")

def filter_and_sort_prs(prs):
    filtered_prs = []
    
    for pr in prs:
        repo_full_name = pr["repository"]["nameWithOwner"]
        
        # ONLY keep the PR if it belongs to a repository in our TARGET_REPOS list
        if repo_full_name in TARGET_REPOS:
            filtered_prs.append(pr)
    
    # Sort the filtered PRs by the repository's star count (highest first)
    filtered_prs.sort(key=lambda x: x["repository"]["stargazerCount"], reverse=True)
    return filtered_prs

def generate_table_string(pr_list):
    table = "| Pull Request | Repository | 🌟 Stars | 🍴 Forks | 💬 Comments |\n"
    table += "|---|---|:---:|:---:|:---:|\n"
    
    for pr in pr_list:
        title = pr["title"].replace("|", "\\|") 
        url = pr["url"]
        repo = pr["repository"]["nameWithOwner"]
        stars = pr["repository"]["stargazerCount"]
        forks = pr["repository"]["forkCount"]
        comments = pr["comments"]["totalCount"]
        
        table += f"| [{title}]({url}) | [{repo}](https://github.com/{repo}) | {stars} | {forks} | {comments} |\n"
        
    return table

def format_markdown_output(prs):
    if not prs:
        return "_No merged PRs found for the target repositories._\n"

    # Split into Top 5 and the rest
    top_prs = prs[:TOP_COUNT]
    other_prs = prs[TOP_COUNT:]

    # Build the main section for the Top 5
    content = "### 🏆 Top Contributions\n\n"
    content += generate_table_string(top_prs)

    # If there are more than 5, wrap the rest in a collapsible <details> tag
    if other_prs:
        content += "\n<details>\n"
        content += "<summary><b>Click to view more contributions</b></summary>\n<br>\n\n"
        content += generate_table_string(other_prs)
        content += "\n</details>\n"

    return content

def update_readme(new_content):
    with open("README.md", "r", encoding="utf-8") as file:
        readme_contents = file.read()

    # Regex to find the space between the markers
    pattern = re.compile(r"(<!-- START_MERGED_PRS -->\n).*?(\n<!-- END_MERGED_PRS -->)", re.DOTALL)
    
    # Replace the old content with the newly generated markdown
    updated_readme = pattern.sub(rf"\g<1>{new_content}\g<2>", readme_contents)

    with open("README.md", "w", encoding="utf-8") as file:
        file.write(updated_readme)

if __name__ == "__main__":
    print("Fetching merged PRs...")
    raw_prs = fetch_prs()
    
    if not raw_prs:
         print("No merged PRs found.")
    else:
        print("Filtering for Target Repos and sorting...")
        target_prs = filter_and_sort_prs(raw_prs)
        
        if not target_prs:
            print("No PRs matched your TARGET_REPOS list.")
            # We can write an empty state to the README if desired
            update_readme("_No PRs matched the target repository list._\n")
        else:
            print("Formatting Markdown output...")
            markdown_output = format_markdown_output(target_prs)
            print("Updating README.md...")
            update_readme(markdown_output)
            print("Successfully updated README!")