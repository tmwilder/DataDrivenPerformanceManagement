import argparse
import os
import os.path as op
import random
import shutil
import subprocess

from _datetime import datetime, timedelta
from typing import List


def get_times_for_day(today: datetime, mean_commits: int) -> List[datetime]:
    how_productive_are_we_today = round(random.normalvariate(mean_commits, (mean_commits/3)))
    return sorted([
        datetime(
            year=today.year,
            month=today.month,
            day=today.day,
            hour=random.randrange(0, 23),
            minute=random.randrange(0, 59),
            second=random.randrange(0, 59)
        )
        for _ in range(how_productive_are_we_today)
    ], reverse=True)


def get_all_times(first_day: datetime, days_back: int, mean_commits: int) -> List[datetime]:
    all_times = []
    for x in range(days_back):
        day_to_assign = first_day - timedelta(days=x)
        times_for_day = get_times_for_day(today=day_to_assign, mean_commits=mean_commits)
        all_times.extend(times_for_day)
    return all_times


def create_repo(author_email: str, author_name: str, repo_name="verylegitimaterepository"):
    current_dir = op.abspath(op.dirname(op.realpath(__file__)))
    repo_path = op.join(current_dir, repo_name)
    readme_path = op.join(current_dir, "GENERATED_README.MD")
    try:
        shutil.rmtree(repo_path)
    except FileNotFoundError:
        pass
    os.mkdir(repo_path)
    shutil.copy(readme_path, op.join(repo_path, "README.md"))
    print(subprocess.check_output(["git", "init", repo_path]))
    print(subprocess.check_output(["git", "add", "README.md"], cwd=repo_path), )
    print(
        subprocess.check_output(
            ["git", "commit", "--author", "'{} <{}>'".format(author_name, author_email), "-m",
                "'Initial commit. Much productivity to follow.'"],
            cwd=repo_path
        )
    )
    print(subprocess.check_output(["git", "branch", "-m", "master", "main"], cwd=repo_path))


def add_commits(author_email: str, author_name: str, repo_name: str, all_times: List[datetime]):
    repo_path = op.join(op.abspath(op.dirname(op.realpath(__file__))), repo_name)
    for commit_time in reversed(all_times):
        print(
            subprocess.check_output(
                ["git", "commit", "--allow-empty", "--author", "'{} <{}>'".format(author_name, author_email),
                    "-m", "'Very productive commit made by: {} <{}> at: {}.'".format(
                        author_name,
                        author_email,
                        commit_time.isoformat())],
                cwd=repo_path,
                env={
                    "GIT_COMMITTER_NAME": author_name,
                    "GIT_COMMITTER_EMAIL": author_email,
                    "GIT_AUTHOR_NAME": author_name,
                    "GIT_AUTHOR_EMAIL": author_email,
                    "GIT_COMMITTER_DATE": commit_time.isoformat(),
                    "GIT_AUTHOR_DATE": commit_time.isoformat()
                }
            )
        )


def main(days_back: int, mean_commits: int, author_email: str, author_name: str, repo_name: str):
    today = datetime.today()
    all_times = get_all_times(first_day=today, days_back=days_back, mean_commits=mean_commits)
    repo_name = repo_name.replace(".", "")
    create_repo(author_email=author_email, author_name=author_name, repo_name=repo_name)
    add_commits(author_email=author_email, author_name=author_name, repo_name=repo_name, all_times=all_times)
    return []


def parse_args():
    parser = argparse.ArgumentParser(description='Demonstrate your ninja skills.')
    parser.add_argument('-n', '--author-name', required=True, type=str, help='Your GitHub user name.')
    parser.add_argument('-e', '--author-email', required=True, type=str, help='Your GitHub email address.')
    parser.add_argument('-d', '--days-back', required=False, default=90, type=int,
                        help='For how many days have you been killing it?')
    parser.add_argument('-c', '--average-commits-per-day', required=False, default=15, type=int,
                        help='How much hacking, on average, occurred per day?')
    parser.add_argument('-r', '--repo-name', required=False, default="synergisticvelocity", type=str,
                        help='How much hacking, on average, occurred per day?')
    return vars(parser.parse_args())


if __name__ == '__main__':
    args = parse_args()
    arg_days_back = args["days_back"]
    arg_author_email = args["author_email"]
    arg_author_name = args["author_name"]
    arg_average_commits_per_day = args["average_commits_per_day"]
    arg_repo_name = args["repo_name"]
    main(
        days_back=arg_days_back,
        mean_commits=arg_average_commits_per_day,
        author_email=arg_author_email,
        author_name=arg_author_name,
        repo_name=arg_repo_name
    )
