# Git for Noobs like us
*Written by Sherman (hence you can blame him)*

//TODO: write cherry-picking
//TODO: write checking out branches 
//TODO: write how to use debug and advanced Pycharm functions

This document is a (hopefully) easy to understand way to get Git up and running. 

To browse the remote repository, go here (there's another URL for the git setup side): 
[HERE](https://github.com/FishOuttaWotah/EPA1352-G07/tree/main) 


## TODO reset interpreter section and usage
## Command References (WIP)

## Getting started (Beta)
First, you'll need a GitHub account. This is needed to access the remote (online) repository and also link it with Pycharm so you can sync everyone's work. `BIG CAVEAT: there may be some steps missing in this guide, let me (Sherman) know if you can't follow`.

### Pycharm access
To give Pycharm access, here's the TLDR from [Pycharm's page](https://www.jetbrains.com/help/pycharm/github.html#register-account):
- go to File/Settings, and then Version Control/Github, you should find an empty list with a + sign on the top right corner. 
- Two ways of doing: 
    - Click + and log into your Github account. You now need to create an access 'token' on your account so that Pycharm will get access to your account (like an ID).  
    - Alternatively, you can also create a token first, and then just use 'log in via token' to gain access. 
- Next, you'll need to be a collaborator (aka admin) of this specific repository. Then give me (Sherman) either email or username so I can add you. You might need to confirm your access via a link in your email.

- There are two ways to get the repository onto your computer. If you have the A3 files on your computer, try #2 and see if it works for you:
    - (#1) In File Explorer, create an empty folder and open as a Pycharm project. Go to the VCS tab in Pycharm and find 'get from Version Control'. Here, input this link to  the repository: <https://github.com/FishOuttaWotah/EPA1352-G07.git>. Pycharm would ask you if you want to 'clone' the repository onto the drive, click yes, and Pycharm then downloads the files from the repository for you.
    - (#2) If you already have the A3 files, you can try opening that directory as a Pycharm project. Go to 'get from Version Control' and input the link <https://github.com/FishOuttaWotah/EPA1352-G07.git>. Pycharm should ask you whether you want to 'merge'/'clone' the repository onto your computer, click yes *(on your own risk/ op eigenrisico!)*. What it *should* do is just update the your project directory with the newer items I've added (a readme file and a NetworkX_sandbox.py file)
- If the import/clone/merge process is successful, you should see something like A2 and A3 folders in your project folder. A2 is just the leftover project scripts for reference.

**Note: you'll need to redo your run settings, since it is blank for every new project.** To do so, go to the script you plan to run, and create a 'run configuration', which defines specific developer-level settings for running the scripts. We only want to run a specific file with a specific Python version, so here's some things you need to do:
- add a run configuration (+ icon), find the Python template under the Templates dropdown
- input the directory path to your script 
- check your Python version is set correctly (especially if you have different versions and environments like the conda thing we did). There's also the setting 'run with Python console', turn it on if you prefer (see Pycharm tips why you should).
- maybe put a name for it (doesn't really matter) and save the configuration.

The convenient thing about the run config setting is that you can also run it for different files. In the editor for the script you want to run, just right click and look for 'run <runConfigName>', and Pycharm will run that file with the run settings.

## Git Basics (Beta)
Now, you should have an extended Pycharm interface, with extra git commands in the VCS tab, extra popout menus on the left and bottom, such as 'commit', 'pull requests', 'Git'.

Whenever you type anything new in Pycharm now, it only is edited for your version of the files (and not for everyone else). 

### Getting updated (Pull/Update)
To **update** your local files, go to VCS/update project, and you should get a choice of Merge or Rebase. Usually, you'll need only to Merge it (takes anything that's changed and insert into your code). Sometimes there might be conflicts if you have something different from the repository's, and Pycharm should open a window to show you side-by-side. You can then just choose which parts you want to keep or not (this sentence may be expanded later).

### Updating the project for others (Commits & Push)
If you want to update the project, you go to the 'commit' tab (should be on the left). There should be a choice called 'Default Changelist', and under it should be the files you've changed/added. Make sure they are ticked, and there should be a type-able space above the Commit button at the bottom. This is the commit comment box, where you write what you've done for this update. 

Click 'commit' and your current work (for the files you chose) would be saved at this state. It is like a save file in video games, and if you want to go back, you can go to the Git window (at the bottom) and see your commit history (and go back to either). NOTE: the remote repository is still not updated yet, so continue on to Push.

**'Pushing'** is you updating the repository, and others can then update their versions with what you've done. Make sure you have the 'build' branch on (instead of 'main', see Branches' first paragraph below), what it does is it updates the remote repository with all of your commits to that 'build' branch. After pushing, everyone should be able to see your update for that specific branch.

Pycharm also has the option to 'push and commit' in the Commit Tab, so you can just update in a single move. 
 
### Working with different versions (Branches)
On the right bottom of Pycharm, you should see a branch-looking icon with 'main' on it, to the right of your Python interpreter. Make sure it is set to 'build' (or anything other than 'main'). This means whatever commits/pushes you do will be for that branch. 

Branches are duplicates of the same repository, so you can experiment and test new features without breaking the original. Updating 'main' branch is reserved for verified builds, when we've tested them and are happy with it. As collaborators, you should be able to create branches and merge them with other branches. 

## Common issues you'll encounter
// Merge request & merging conflicts
// OHNOIVECOMMITTEDTOTHEWRONGBRANCH

# PyCharm: some fancy stuff (Beta)
PyCharm has some real good things that even noobs like us can really appreciate. This is a guide for them. Some simple tricks first:
- shift+alt+(up/down) to move a line up or down
- shift+/ to comment/uncomment
- if you aren't highlighting text, cut/copy actions copy the entire line 

## Renaming stuff (code **refactoring**) {shift+f6}
To rename a variable that's present in the script (maybe also in other files, in comments and strings), highlight the variable and find 'refactor' in the top bar or right click menu. Look for 'rename', and type in the new variable name. If the option's available, check the tick box to check in comments and strings, and also the dropdown tab to specify whether to include searching for this variable in other project files. 

Sometimes the refactoring dialog would show you the usages of this variable in other files, don't panic, just check if the usages make sense and don't conflict with other similar-sounding variables, and continue with the refactor. The keyboard shortcut (shift+f6 or whatever you have) may bring up a different refactor dialog as well, so play around with it but be ready to undo any damage.

## Code **suggestions** 
When you fill in code, you'll get a dropdown of suggestions from PyCharm. You don't need to type out the full variable name, but just part of the name that's easily identifiable. EG, if you're working in a Pandas script with lots of DataFrames starting with 'df', if you want to access 'df_not_hentai', just start typing 'hent' and Pycharm probably knows what you want.

Debug tip: code suggestions are drawn from what items the space you're typing in could access (class, functions, attributes), so if Pycharm doesn't suggest anything that you know you have, it's likely that you cannot access it in that area, probably an import issue, a typo, or no access (especially in functions and classes).

## 'Folding' code segments you aren't interested in (code **folding**) {ctrl+.}

 
// run with console
// run with debug
// code refactoring
// code folding
// code suggestions
// code cleanup

