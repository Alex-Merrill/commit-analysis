import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import sys
import re
import git


def main(data):
    # parse file and return list of commits
    commits = parse_data(data)

    # generate pandas data frame from list of commits
    df = pd.DataFrame.from_records(commits)

    # visualize data
    visualize(df)


def parse_data(data):
    commits = []
    for line in data:
        # print(line)
        commit_arr = [i.strip() for i in line.split(",")]

        # figure out when commit message ends in commit_arr
        # next element after commit message is files changed
        files_changed_index = -1
        message = ""
        for i in range(5, len(commit_arr)):
            changed = re.search("files changed", commit_arr[i]) or re.search("file changed", commit_arr[i])
            if not changed:
                message += commit_arr[i]
            else:
                files_changed_index = i
                break

        # get number of files changed
        files_changed = int(commit_arr[files_changed_index].split(" ")[0])

        # get number of insertions/deletions
        insertions = 0
        deletions = 0
        for i in range(files_changed_index+1, len(commit_arr)):
            if re.search("insertions", commit_arr[i]) or re.search("insertion", commit_arr[i]):
                insertions = int(commit_arr[i].split(" ")[0])
            elif re.search("deletions", commit_arr[i]) or re.search("deletion", commit_arr[i]):
                deletions = int(commit_arr[i].split(" ")[0])

        # construct newLine object
        newLine = {'head': commit_arr[0],
                   'user': commit_arr[1],
                   'email': commit_arr[2],
                   'date': commit_arr[3]+" "+commit_arr[4],
                   'content': message,
                   'files': files_changed,
                   'insert': insertions,
                   'delete': deletions}

        # make commit
        commits.append(newLine)

    return commits


def visualize(df):
    mpl.style.use('ggplot')
    insertDeleteCount = df.groupby('user').sum()
    insertDeleteCount = insertDeleteCount.sort_values('insert', ascending=False)
    insertDeleteCount.plot.bar(figsize=(9, 8), title="File Changes/Insertions/Deletions by user")
    plt.legend(["Files Changed", "Insertions", "Deletions", ])
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Command Line Arguments:")
        print("python3 logParser.py 'path of repo'")
    else:
        repo = git.Repo(sys.argv[1])
        log = repo.git.log("--pretty=format:'\"%h\",\"%an\",\"%ae\",\"%aD\",\"%s\",'",
                           "--shortstat", "--no-merges")
        data = [i.replace("\n", "").replace("'", "").replace('"', "") for i in log.split("\n\n")]

        main(data)
