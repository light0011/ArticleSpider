from git import Repo

repo = Repo("./")
g = repo.git
print(g.status())
print(g.add("--all"))
print(g.commit("-m \"fix bug\""))

# index.add(repo.untracked_files)
# newcommit=index.commit('Regular')
# origin=repo.remotes.origin
# origin.push()
