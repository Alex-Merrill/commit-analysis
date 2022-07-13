import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

import sys
import os
import re
import csv



class Commit():

    def __init__(self, head, user, email, date, content, files, insert=None, delete=None):
        self.head = head
        self.user = user
        self.email = email
        self.date = date
        self.content = content
        self.files = files
        self.insert = insert
        self.delete = delete


def run(file_name: str):
    # parse file and return list of commits
    data = parse_file(file_name)

    # generate csv file from list of commits
    make_csv(data)

    # turn csv into pandas dataframe with proper column names
    data_frame = pd.read_csv("data.csv", header=None)
    data_frame.rename(columns={0: 'head', 1: 'user', 2: 'email', 3: 'date', 4: 'content', 5: 'files', 6: 'insert', 7: 'delete'}, inplace=True)

    # visualize data
    visualize(data_frame)
    
    
def visualize(df):
    mpl.style.use('ggplot')
    # print(df)
    # df[(df["user"] == "wkelley11") & (df["insert"] >= 40) ]
    insertDeleteCount = df.groupby('user').sum()
    insertDeleteCount = insertDeleteCount.sort_values('insert', ascending=False)
    insertDeleteCount.plot.bar(figsize=(9,8), title="Insert/Delete Count by User")
    plt.legend(["Insertions", "Deletions"])
    plt.show()

def parse_file(file_name: str) -> list:
    try:
        with open(file_name) as data:
            lines = data.readlines()
            commits = []
            for line in lines:
                line = line.replace("\"", "")
                line = line.split(",")

                # get commit message
                filesInd = -1
                message = ""
                for i in range(5, len(line)):
                    changed = re.search("files changed", line[i]) or re.search("file changed", line[i])
                    if not changed:
                        message += line[i]
                    else:
                        filesInd = i
                        break
                
                insertions = ""
                deletions = ""
                # check whats after
                for i in range(filesInd+1, len(line)):
                    if re.search("insertions", line[i]) or re.search("insertion", line[i]):
                        insertions = line[i]
                    if re.search("deletions", line[i]) or re.search("deletion", line[i]):
                        deletions = line[i]
                
                filesChanged = line[filesInd].replace("\t ", "")

                insertions = insertions.replace("\t", "")
                insertions = insertions.replace("\n", "")[1:]
                insertions = insertions.split(" ")[0]

                deletions = deletions.replace("\t", "")
                deletions = deletions.replace("\n", "")[1:]
                deletions = deletions.split(" ")[0]
                
                if line[1] == 'Alex Merrill':
                    line[1] = 'Alex-Merrill'

                # construct newLine object
                newLine = { 'head': line[0],
                            'user': line[1],
                            'email': line[2],
                            'date': line[3]+line[4],
                            'content': message,
                            'files': filesChanged,
                            'insert': insertions,
                            'delete': deletions }
                
                # make commit
                commits.append(Commit(**newLine))

            print("File processed")
            return commits
    except FileNotFoundError:
        print("The file was not found")

def make_csv(data: list):
    try:
        with open('data.csv', 'w') as f:
            writer = csv.writer(f)
            for dat in data:
                writer.writerow([dat.head, dat.user, dat.email, dat.date, dat.content, dat.files, dat.insert, dat.delete])
    except BaseException as e:
        print('BaseException:', 'data.csv')
    else:
        print('Data has been loaded successfully !')




if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Command Line Arguments:")
        print("python3 s3upload.py 'absolute file path'")
    else:
        run(sys.argv[1])
        

