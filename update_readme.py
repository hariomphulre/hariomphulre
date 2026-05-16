# import os
# import re
# import requests

# USERNAME = "hariomphulre"
# TOKEN = os.environ.get("GH_TOKEN")

# # --- CONFIGURATION ---
# TARGET_REPOS = [
#     "facebook/react",               
#     "torvalds/linux", 
#     "some-org/some-awesome-repo",
#     "archlinux/archinstall",
#     "nlohmann/json",
# ]

# TOP_COUNT = 5
# # ---------------------

# if not TOKEN:
#     raise ValueError("GH_TOKEN environment variable is not set.")

# headers = {"Authorization": f"Bearer {TOKEN}"}

# query = """
# query {
#   user(login: "%s") {
#     pullRequests(states: MERGED, first: 100, orderBy: {field: CREATED_AT, direction: DESC}) {
#       nodes {
#         title
#         url
#         bodyText
#         additions
#         deletions
#         repository {
#           nameWithOwner
#           stargazerCount
#           forkCount
#         }
#         comments {
#           totalCount
#         }
#         reviews {
#           totalCount
#         }
#       }
#     }
#   }
# }
# """ % USERNAME

# def fetch_prs():
#     response = requests.post("https://api.github.com/graphql", json={"query": query}, headers=headers)
#     if response.status_code == 200:
#         return response.json()["data"]["user"]["pullRequests"]["nodes"]
#     else:
#         raise Exception(f"API request failed: {response.text}")

# def filter_and_sort_prs(prs):
#     filtered_prs = []
    
#     for pr in prs:
#         repo_full_name = pr["repository"]["nameWithOwner"]
        
#         if repo_full_name in TARGET_REPOS:
#             filtered_prs.append(pr)
            
#     filtered_prs.sort(key=lambda x: x["repository"]["stargazerCount"], reverse=True)
#     return filtered_prs

# def generate_card_string(pr_list):
#     content = ""
#     for pr in pr_list:
#         # Escape brackets in titles so it doesn't break markdown links
#         title = pr["title"].replace("[", "\\[").replace("]", "\\]")
#         url = pr["url"]
#         repo = pr["repository"]["nameWithOwner"]
#         stars = pr["repository"]["stargazerCount"]
#         forks = pr["repository"]["forkCount"]
#         additions = pr["additions"]
#         deletions = pr["deletions"]
        
#         # Sum up timeline comments and code reviews to get the real count
#         total_comments = pr["comments"]["totalCount"] + pr["reviews"]["totalCount"]
        
#         # Get PR description and truncate it cleanly to match the screenshot look
#         body = pr["bodyText"].replace("\n", " ").strip()
#         if len(body) > 130:
#             body = body[:127] + "..."
#         if not body:
#             body = "_No description provided._"

#         # Official GitHub Octicons served via Iconify API (allows us to color them without CSS)
#         icon_merge = '<img src="https://api.iconify.design/octicon/git-merge-16.svg?color=%238250df" width="16" height="16" alt="merged" />'
#         icon_repo = '<img src="https://api.iconify.design/octicon/repo-16.svg?color=%238b949e" width="16" height="16" alt="repo" />'
#         icon_star = '<img src="https://api.iconify.design/octicon/star-16.svg?color=%238b949e" width="14" height="14" alt="stars" />'
#         icon_fork = '<img src="https://api.iconify.design/octicon/repo-forked-16.svg?color=%238b949e" width="14" height="14" alt="forks" />'
#         icon_comment = '<img src="https://api.iconify.design/octicon/comment-16.svg?color=%238b949e" width="14" height="14" alt="comments" />'

#         # Build the Native Timeline UI
#         content += f"{icon_repo} **Created a pull request in [{repo}](https://github.com/{repo})**\n\n"
        
#         # Wrapping in blockquotes (>) creates the left vertical timeline line
#         content += f"> {icon_merge} &nbsp; **[{title}]({url})**\n>\n"
#         content += f"> {body}\n>\n"
#         content += f"> `+{additions}` `-{deletions}` lines changed &nbsp;•&nbsp; {icon_star} {stars} &nbsp; {icon_fork} {forks} &nbsp;•&nbsp; {icon_comment} {total_comments}\n\n"
#         content += "<br>\n\n"
        
#     return content

# def format_markdown_output(prs):
#     if not prs:
#         return "_No merged PRs found for the target repositories._\n"

#     top_prs = prs[:TOP_COUNT]
#     other_prs = prs[TOP_COUNT:]

#     content = generate_card_string(top_prs)

#     if other_prs:
#         content += "\n<details>\n"
#         content += "<summary><b>Click to view more contributions</b></summary>\n<br>\n\n"
#         content += generate_card_string(other_prs)
#         content += "\n</details>\n"

#     return content

# def update_readme(new_content):
#     with open("README.md", "r", encoding="utf-8") as file:
#         readme_contents = file.read()

#     header_match = re.search(r'(#{1,6}\s*.*?Top Contributions.*?)\n', readme_contents, re.IGNORECASE)
    
#     if not header_match:
#         print("Error: Could not find the 'Top Contributions' heading in README.md")
#         return

#     start_idx = header_match.end()

#     next_divider_match = re.search(r'\n\s*---\s*(?=\n|$)', readme_contents[start_idx:])
    
#     if next_divider_match:
#         end_idx = start_idx + next_divider_match.start()
#         after_content = readme_contents[end_idx:]
#     else:
#         after_content = "\n" 

#     updated_readme = (
#         readme_contents[:start_idx] 
#         + "\n" 
#         + new_content 
#         + "\n" 
#         + after_content
#     )

#     with open("README.md", "w", encoding="utf-8") as file:
#         file.write(updated_readme)

# if __name__ == "__main__":
#     print("Fetching merged PRs...")
#     raw_prs = fetch_prs()
    
#     if not raw_prs:
#          print("No merged PRs found.")
#     else:
#         print("Filtering for Target Repos and sorting...")
#         target_prs = filter_and_sort_prs(raw_prs)
        
#         if not target_prs:
#             print("No PRs matched your TARGET_REPOS list.")
#             update_readme("_No PRs matched the target repository list._\n")
#         else:
#             print("Formatting Markdown output...")
#             markdown_output = format_markdown_output(target_prs)
#             print("Updating README.md...")
#             update_readme(markdown_output)
#             print("Successfully updated README!")

#------------------------------------------------------------------------------------------------------

import os
import re
import requests
from datetime import datetime

USERNAME = "hariomphulre"
TOKEN = os.environ.get("GH_TOKEN")

# --- CONFIGURATION ---
TARGET_REPOS = [
    "facebook/react",               
    "torvalds/linux", 
    "some-org/some-awesome-repo",
    "archlinux/archinstall",
    "nlohmann/json",
]

TOP_COUNT = 5
# ---------------------

if not TOKEN:
    raise ValueError("GH_TOKEN environment variable is not set.")

headers = {"Authorization": f"Bearer {TOKEN}"}

query = """
query {
  user(login: "%s") {
    pullRequests(states: MERGED, first: 100, orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        title
        url
        bodyText
        additions
        deletions
        createdAt
        repository {
          nameWithOwner
          stargazerCount
          forkCount
        }
        comments {
          totalCount
        }
        reviews {
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
        
        if repo_full_name in TARGET_REPOS:
            filtered_prs.append(pr)
            
    filtered_prs.sort(key=lambda x: x["repository"]["stargazerCount"], reverse=True)
    return filtered_prs

def generate_card_string(pr_list):
    content = ""
    for pr in pr_list:
        title = pr["title"].replace("[", "\\[").replace("]", "\\]")
        url = pr["url"]
        repo = pr["repository"]["nameWithOwner"]
        stars = pr["repository"]["stargazerCount"]
        forks = pr["repository"]["forkCount"]
        additions = pr["additions"]
        deletions = pr["deletions"]
        
        total_comments = pr["comments"]["totalCount"] + pr["reviews"]["totalCount"]
        
        date_obj = datetime.strptime(pr["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
        date_str = f"{date_obj.strftime('%b')} {date_obj.day}, {date_obj.year}"
        
        body = pr["bodyText"].replace("\n", " ").strip()
        if len(body) > 130:
            body = body[:127] + "..."
            
        if not body:
            body = "_No description provided._"
        else:
            body = re.sub(r'#(\d+)', rf'[#\1](https://github.com/{repo}/pull/\1)', body)

        # Official Icons + New Grey Dot Icon
        icon_merge = '<img src="https://api.iconify.design/octicon/git-merge-16.svg?color=%238250df" width="16" height="16" alt="merged" />'
        icon_repo = '<img src="https://api.iconify.design/octicon/repo-16.svg?color=%238b949e" width="16" height="16" alt="repo" />'
        icon_star = '<img src="https://api.iconify.design/octicon/star-16.svg?color=%238b949e" width="14" height="14" alt="stars" />'
        icon_fork = '<img src="https://api.iconify.design/octicon/repo-forked-16.svg?color=%238b949e" width="14" height="14" alt="forks" />'
        icon_comment = '<img src="https://api.iconify.design/octicon/comment-16.svg?color=%238b949e" width="14" height="14" alt="comments" />'
        icon_dot = '<img src="https://api.iconify.design/octicon/dot-fill-16.svg?color=%238b949e" width="12" height="12" alt="dot" />'

        # Updated First Line: Reverted the font for the date, replaced the text dot with the grey SVG dot
        content += f"{icon_repo} Created a pull request in **[{repo}](https://github.com/{repo})** &nbsp;{icon_dot}&nbsp; {date_str}\n"
        content += f"> {icon_merge} &nbsp; **[{title}]({url})**\n>\n"
        content += f"> {body}\n>\n"
        content += f"> `+{additions}` `-{deletions}` lines changed &nbsp;{icon_dot}&nbsp; {icon_star} {stars} &nbsp; {icon_fork} {forks} &nbsp;{icon_dot}&nbsp; {icon_comment} {total_comments}\n\n"
        content += "<br>\n\n"
        
    return content

def format_markdown_output(prs):
    if not prs:
        return "_No merged PRs found for the target repositories._\n"

    top_prs = prs[:TOP_COUNT]
    other_prs = prs[TOP_COUNT:]

    content = generate_card_string(top_prs)

    if other_prs:
        content += "\n<details>\n"
        content += "<summary><b>Click to view more contributions</b></summary>\n<br>\n\n"
        content += generate_card_string(other_prs)
        content += "\n</details>\n"

    return content

def update_readme(new_content):
    with open("README.md", "r", encoding="utf-8") as file:
        readme_contents = file.read()

    header_match = re.search(r'(#{1,6}\s*.*?Top Contributions.*?)\n', readme_contents, re.IGNORECASE)
    
    if not header_match:
        print("Error: Could not find the 'Top Contributions' heading in README.md")
        return

    start_idx = header_match.end()

    next_divider_match = re.search(r'\n\s*---\s*(?=\n|$)', readme_contents[start_idx:])
    
    if next_divider_match:
        end_idx = start_idx + next_divider_match.start()
        after_content = readme_contents[end_idx:]
    else:
        after_content = "\n" 

    updated_readme = (
        readme_contents[:start_idx] 
        + "\n" 
        + new_content 
        + "\n" 
        + after_content
    )

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
            update_readme("_No PRs matched the target repository list._\n")
        else:
            print("Formatting Markdown output...")
            markdown_output = format_markdown_output(target_prs)
            print("Updating README.md...")
            update_readme(markdown_output)
            print("Successfully updated README!")