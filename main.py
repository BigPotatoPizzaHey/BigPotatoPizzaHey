import os
import json
from pathlib import Path
from typing import TypedDict
from github import Github, Auth, ContentFile, Issue

token = os.environ["GH_TOKEN"]
auth = Auth.Token(token)
gh = Github(auth=auth)

data_file = Path("data.json")
class Schema(TypedDict):
    score: int 
    scorers: dict[str, int]

def get_data() -> Schema:
    return json.load(data_file.open())

def write_data(content: Schema) -> None:
    json.dump(content, data_file.open("w"))

def main():
    print("Starting...")
    repo = (gh.get_user("BigPotatoPizzaHey")
        .get_repo("BigPotatoPizzaHey"))
    
    for issue in repo.get_issues(
        state="open",
        labels=["score"]
    ):
        resolve(issue)

def resolve(issue: Issue.Issue):
    body = issue.body.lower()

    up = "up" in body
    down = "down" in body
    score_change = up - down

    username = issue.user.name if issue.user.name else ""
    data = get_data()
    data["score"] += score_change
    data["scorers"][username] = data["scorers"].get(username, 0) + score_change
    write_data(data)
    
    issue.create_comment(f"""\
You +='ed by `{score_change}`!
New score: {data["score"]}
You've scored: {data["scorers"][username]}!
""")
    issue.edit(state="closed")


if __name__ == "__main__":
    main()
