# Git for Noobs like us
Written by Sherman (hence you can blame him)

This document is a (hopefully) simple and concise way to get Git up and running. 

To browse the remote repository, go here (don't use this URL for setting up sync!): 
[to repo](https://github.com/FishOuttaWotah/AdvSim-G07/tree/feature) 

## Command References (WIP)

## Getting started (WIP)
First, you'll need a GitHub account. This is needed to access the remote (online) repository and also link it with Pycharm so you can sync everyone's work. `BIG CAVEAT: there may be some steps missing in this guide, let me (Sherman) know if you can't follow`.

### Pycharm access
To give Pycharm access, here's the TLDR from [ref](https://www.jetbrains.com/help/pycharm/github.html#register-account):
- go to File/Settings, and then Version Control/Github, you should find an empty list with a + sign on the top right corner. 
- Two ways of doing: 
    - Click + and log into your Github account. You now need to create an access 'token' on your account so that Pycharm will get access to your account (like an ID).  
    - Alternatively, you can also create a token first, and then just use 'log in via token' to gain access. 
- Next, you'll need to be a collaborator (aka admin) of this specific repository. Then give me (Sherman) either email or username so I can add you. You might need to confirm your access via a link in your email.

- (choice #1) In File Explorer, create an empty folder and open as a Pycharm project. Go to the VCS tab in Pycharm and find 'get from Version Control'. Here, you input this link to access the repository I made: <https://github.com/FishOuttaWotah/EPA1352-G07.git>. Pycharm would probably ask you if you want to 'clone' the repository onto the drive, click yes.
- (choice #2) If you already have the A3 files, you can try opening that directory as a Pycharm project. Go to 'get from Version Control' and input the link <https://github.com/FishOuttaWotah/EPA1352-G07.git>. Pycharm should ask you whether you want to 'merge'/'clone' the repository onto your computer, click yes (on your own risk/ op eigenrisico!). What it *should* do is just update the your project directory with the newer items I've added (a readme file and a NetworkX_sandbox.py file)
- If the import/clone/merge process is successful, you should see something like A2 and A3 folders in your project folder. A2 is just the leftover project scripts (without the scenario.csv because I'm too lazy to download them separately from DeepNote).  

## Git Basics (WIP)
Now you should have an extended Pycharm interface, with extra git commands in the VCS tab, extra popout menus on the left and bottom, such as 'commit', 'pull requests', 'Git'.

Whenever you type anything new in Pycharm now, it only is edited for your version of the files (and not for everyone else). 

### Getting updated (Pull/Update)
To update, go to VCS/update project, and you should get a choice of Merge or Rebase. Usually, you'll need only to Merge it (takes anything that's changed and insert into your code). Sometimes there might be conflicts if you have something different from the repository's, and Pycharm should open a window to show you side-by-side. You can then just choose which parts you want to keep or not (this sentence may be expanded later).

### Updating the project for others (Commits & Push)
If you want to update the project, you go to the 'commit' tab (should be on the left). There should be a choice called 'Default Changelist', and under it should be the files you've changed/added. Make sure they are ticked, and there should be a type-able space above the Commit button at the bottom. This is the commit comment box, where you write what you've done for this update. 

Click 'commit' and your current work (for the files you chose) would be saved at this state. It is like a save file in video games, and if you want to go back, you can go to the Git window (at the bottom) and see your commit history (and go back to either). NOTE: the remote repository is still not updated yet, so continue on to Push.

Push-ing is you updating the repository, and others can then update their versions with what you've done. Make sure you have the 'build' branch on (instead of 'main', see Branches below), what it does is it updates the remote repository with all of your commits to that 'build' branch. 
 
### Working with different versions (Branches)
On the right bottom of Pycharm, you should see a branch-looking icon with a colour circle (probably green, yellow or red) with 'main' on it. Make sure it is set to 'build' (or anything other than 'main'). 

Branches are duplicates of the same repository, so you can experiment and test new features without breaking the original. Updating 'main' branch is reserved for very bulletproof/watertight builds, when we've tested and are happy with it.
