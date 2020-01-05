#!/usr/bin/python3
import os
import git
import requests
import concurrent.futures
import argparse
from collections import defaultdict
from bs4 import BeautifulSoup
import csv

parser=argparse.ArgumentParser(description="This tool outputs two csv files with Commit messages and Commit page comments against it's CommitID")
parser.add_argument('-u','--u',type=str,help="Provide Github repo url",required=True)
args=parser.parse_args()
commit_list=[]
final_list_branches=[]
remote_branches = []
commit_comments_list=[]

def version_info():
	VER = 'Commit Hunter v1.0 - \033[033mFind Commit messages and Commit Page Comments for Github repo \033[0m'
	AUTH = 'Author: \033[033mVijay Adapa - https://securityboy.com/\033[0m'
	print(VER)
	print(AUTH)
	print('\033[1;30m================================================\033[0m')

#Checkout the branches in order to access all the branches
def checkout_branches():
    [remote_branches.append(ref.split('/')[1]) for ref in repo.git.branch('-r').split('\n')]
    [repo.git.checkout(branch) for branch in remote_branches[1:]]
    [final_list_branches.append(branch) for branch in repo.branches]

#Taking the repo name provided as input and storing in current directory
if args.u:       
    try:
        param=args.u.split('/')
        git.Repo.clone_from(args.u,os.path.join(os.getcwd(),param[4]))
        repo = git.Repo(os.path.join(os.getcwd(),param[4]))
        checkout_branches()
        version_info()
        
    except AttributeError as e:
        print("provide valid url with -u ")

for branch in final_list_branches:
    
    all_commits = list(repo.iter_commits(branch, max_count=1000)) #adjust max_count as per commit count expected
    for commit in all_commits:
        commit_list.append(commit)
    
uniq_commit=list(set(commit_list)) #uniq commits list

commit_messages_list=[]
commit_results_comments=defaultdict(list)
commit_results_messages=defaultdict(list)

def all_results_func(commit_id):

    base_url=os.path.join(args.u,'commit',str(commit_id))
    src=requests.get(base_url).text
    soup=BeautifulSoup(src,'lxml')
    commit_comments=soup.find_all('task-lists')    
    #Taking the comments on commit page and writing them to csv against each commitid
    for comment in commit_comments:
        commit_results_comments[str(commit_id)].append(comment.p.text)

    with open('output_comments.csv','w') as opfile:
        csv_writer=csv.writer(opfile,delimiter=',')  
        csv_writer.writerow(['COMMIT-ID','COMMIT-COMMENTS'])
        for key,value in commit_results_comments.items():
            csv_writer.writerow([key]+[value])
    #Writing csv output with commit messages against corresponding commitid
    commit_results_messages[str(commit_id)].append([commit_id.message.strip('\n')])
    with open('output_messages.csv','w') as optfile:
        csv_writer=csv.writer(optfile,delimiter=',')  
        csv_writer.writerow(['COMMIT-ID','COMMIT-MESSAGE'])
        for key,value in commit_results_messages.items():
            csv_writer.writerow([key]+[value])           
    
with concurrent.futures.ThreadPoolExecutor() as executor:
    results=executor.map(all_results_func,uniq_commit)

