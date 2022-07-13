#code
git log --pretty=format:'"%h","%an","%ae","%aD","%s",' --shortstat --no-merges | paste - - - > log.txt