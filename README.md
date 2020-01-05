# Commit-Hunter

I've encountered multiple occasions during chained CTF where Hint/Flag hidden in the Github commit messages and the commit page comments with no whatsover content in the repo.This tool has been really useful when there were around 2000 or even more commits across diffrent branches and needs to be dig down to find important lead/Flag in the CTF's.


To Give you an idea how this can easy your life , try finding the following flag ***FLAG{COMMIT-HUNTER}*** in this repository https://github.com/alwaysadapa/jest which is hidden in commits manually and then with this tool.




![example scan](https://www.secureboy.com/wp-content/uploads/2020/01/Screen-Shot-2020-01-05-at-7.56.08-PM-1024x115.png)




The ***-u*** flag  is mandatory and allows you to specify the github repo url.

# Installation

```shell
virtualenv venv
. ./venv/bin/activate
pip install -u -r requirements.txt
```


# Usage

```
usage: commit-hunter.py [-h] [-v] [-u URL]

 arguments:
 
  -h, --help            show this help message and exit
  -u URL, --url URL     Github Repo URL ( Mandatory)


```
On the successful completion , we will get following files ***output_comments.csv*** and ***output_messages.csv*** which will have commit page comments and commit messages tagged against it's commitid respectively.

![Result Flag](https://www.secureboy.com/wp-content/uploads/2020/01/Screen-Shot-2020-01-05-at-11.52.19-PM-300x80.png)

Approach used is blogged here : https://www.secureboy.com/2020/01/commit-hunter-visualizing-hidden-content-in-commits-for-given-github-repo/ . Feel free to raise issues and feature requests if any.
