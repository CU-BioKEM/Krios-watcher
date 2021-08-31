import subprocess
import time
import argparse
import os

parser = argparse.ArgumentParser(description= \
        'Automatically update the Krios-watcher website.')

parser.add_argument('-t', '--time',
                    default=600,
                    dest='wait_time',
                    help='Number of seconds to wait between checks',
                    type=int
                    ))

parser.add_argument('-d', '--directory',
                    required=True
                    dest='directory',
                    help='Absolute path to target directory on Petalibrary or other',
                    type=str
                    ))

parser.add_argument('-p', '--pictures',
                    default=10,
                    dest='num_pics',
                    help='Number of pictures to show on website',
                    type=int
                    ))

parser.add_argument('-g', '--git',
                    default='/home/biokem_manager/git_backup/Krios-watcher/',
                    dest='git_path',
                    help='Path to git repo',
                    type=str
                    ))


args = parser.parse_args()

wait_time = args.wait_time
directory = args.directory
num_pics = args.num_pics

def main():
    subprocess.run(["cd", '"{}"'.format(git_path)])
    start_state()
    while(time_since_last_pic < 120):
        remove_old_pics(num_pics)
        select_pics = select_pics(directory, num_pics)
        copy_to_repo(select_pics)
        push_to_github(num_pics)
        time_since_last_pic = find_time_since_last_pic()
        time.sleep(wait_time)
    clean_up(old_pics)
    return True

def start_state():
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

def find_time_since_last_pic():
    return time_since_last_pic

def select_pics(directory, num_pics):
    selected_pics = []
    files = os.listdir(directory)[-num_pics:]
    for file in files:
        if '.tif' in file:
            selected_pics.append(file)
    return selected_pics

def copy_to_repo(select_pics):
    pic_counter = 0
    for pic in select_pics:
        subprocess.run(["cp",'"{}"'.format(pic), "./'{}'.tif".format(pic_counter)])
    return True

def push_to_github(num_pics):
    pics = [0,(num_pics-1),1]
    for pic in pics:
        subprocess.run(["git", "add", "./'{}'.tif".format(pic)])
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
