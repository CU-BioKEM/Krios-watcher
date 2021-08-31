#!/usr/bin/env python3

import subprocess
import time
import argparse
import os
import shutil

parser = argparse.ArgumentParser(description= \
        'Automatically update the Krios-watcher website.')

parser.add_argument('-t', '--time',
                    default=600,
                    dest='wait_time',
                    help='Number of seconds to wait between checks',
                    type=int
                    )

parser.add_argument('-d', '--directory',
                    required=True,
                    dest='directory',
                    help='Absolute path to target directory on Petalibrary or other',
                    type=str
                    )

parser.add_argument('-p', '--pictures',
                    default=10,
                    dest='num_pics',
                    help='Number of pictures to show on website',
                    type=int
                    )

parser.add_argument('-g', '--git',
                    default='/home/biokem_manager/git_backup/Krios-watcher/',
                    dest='git_path',
                    help='Path to git repo',
                    type=str
                    )

args = parser.parse_args()

wait_time = args.wait_time
directory = args.directory
if directory[-1] is not '/':
    directory = directory+'/'
num_pics = args.num_pics
git_path = args.git_path

def main():
    start_state()
    time_since_last_pic = 50
    while(time_since_last_pic < 120):
        selected_pics = select_pics(directory, num_pics)
        copy_to_repo(selected_pics, directory, git_path)
        push_to_github(selected_pics)
        #time_since_last_pic = find_time_since_last_pic(directory)
        time.sleep(wait_time)
        remove_old_pics(num_pics)
        time_since_last_pic = 130
    #clean_up(old_pics)
    return True

def start_state():
    os.chdir(git_path)
    subprocess.run(["cp", "start_state/README.md", "."])
    subprocess.run(["git", "add", "README.md"])
    subprocess.run(["git", "commit", "-m", "'start state initiated'"])
    subprocess.run(["git", "push", "origin", "main"])
    return "Krios-watcher has begun."

def remove_old_pics(num_pics):
    try:
        subprocess.run(["git", "rm", "--cached", "*.tif"])
        subprocess.run(["git", "commit", "-m", "'automated picture removal'"])
        subprocess.run(["git", "push", "origin", "main"])
    except:
        print("No files to remove.")
    return True

def find_time_since_last_pic(directory):
    return time_since_last_pic

def select_pics(directory, num_pics):
    selected_pics = []
    files = os.listdir(directory)
    files.sort()
    files = files[-num_pics:]
    for file in files:
        if '.tif' in file:
            selected_pics.append(file)
    selected_pics.sort()
    return selected_pics

def copy_to_repo(selected_pics, directory, git_path):
    for pic in selected_pics:
        source = directory+pic
        if os.path.isfile(source):
            shutil.copy(source, git_path)
    return True

def push_to_github(selected_pics):
    for pic in selected_pics:
        subprocess.run(["git", "add", "./{}".format(pic)])
    subprocess.run(["git", "commit", "-m", "'automated picture add'"])
    subprocess.run(["git", "push", "origin", "main"])
    return True

def clean_up(num_pics):
    remove_old_pics(num_pics)
    subprocess.run(["cp", "end_state/README.md", "."])
    subprocess.run(["git", "add", "README.md"])
    subprocess.run(["git", "commit", "-m", "'end state reached'"])
    subprocess.run(["git", "push", "origin", "main"])
    return "Krios-watcher has ended."

if __name__ == '__main__':
    main()
