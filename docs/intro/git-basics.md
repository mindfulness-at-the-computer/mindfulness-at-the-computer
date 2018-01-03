

# Stage

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



## Remote Repository

Please note: The remote also has all the three stages above, but for practical purposes it might be useful to think
of this as the fourth stage

`git status`




