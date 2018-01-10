

# Working with the different stages in Git

Git has a few different stages that a file or a change to a file can be in:

## Working Directory

### `git status`

```
$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

Untracked files:
  (use "git add <file>..." to include in what will be committed)

	new-file.py

```

### `git add`

Using `git add` will move the changes into the staging area

```
git add new-file.py
```


## Staging Area

### `git status`

```
$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

	new file:   new-file.py

```

### `git commit`

This moves the changes into the (local) repository


## Repository

The local repository

### `git status`

```
$ git status
On branch master
Your branch is ahead of 'origin/master' by 1 commit.
  (use "git push" to publish your local commits)
```

### `git push`

```
git push new-file.py
```


## Remote

Please note: Remote also has all the three stages above, but for practical purposes it might be useful to think
of this as the fourth stage

### `git status`

```
$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
nothing to commit, working directory clean
```

***

Good to know:
* Most of the commands in git perform actions locally
