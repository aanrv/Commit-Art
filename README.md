# Commit-Art

Allows user to create designs on GitHub's commit graph.

# Dependencies

Just the obvious: Python and Git.

# How It Works

Given a list of coordinates the user wants highlighted on GitHub's commit graph, the script calculates the corresponding dates.  A Git directory is then created with a series of commits on the corresponding dates. When the repository is pushed to a remote repo on GitHub, the user's desired coordinates will be filled on the commit graph.

Note that only the author date is changed, not the committer date. As far as I know, that seems to be enough to allow you to draw clever and/or humorous things on your commit graph. Also, no environment variables (`GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE`) are directly altered this way.

# Usage

`./commit-art <pointsFile> <dirName> [repoURL]`

- `pointsFile`: A text file containing the coordinates you wish to fill in the commit graph.
- `dirName`: Name of the Git directory to be created.
- `repoURL`: Optionally, the URL to a GitHub repo (`https://github.com/$USERNAME/$REPONAME.git`). If provided, directory will be pushed automatically.

# Directions

1. Create a text file with a list of the points you wish to fill on GitHub's commit graph.

   Sample text file:
   ```
   0,0
   1,1
   2,2
   3,3
   4,4
   ```
   The format is `x,y` separated by newlines. `0,0` is the earliest date (top leftmost point) on the commit graph.
2. Create an empty repository on GitHub (preferrably on an account with no other repositories with commits).
3. Run the script as shown in above.
4. Optional: If `repoURL` was not provided, manually push the directory to the GitHub repository you created in step 2.


