import subprocess
import time
import argparse

parser = argparse.ArgumentParser(description= \
        'Automatically update the Krios-watcher website.')

parser.add_argument('-t', '--time',
                    default=600,
                    dest='wait_time',
                    help='Number of seconds to wait between checks',
                    type=int
                    ))

parser.add_argument('-t', '--time',
                    default=600,
                    dest='wait_time',
                    help='Number of seconds to wait between checks',
                    type=int
                    ))

args = parser.parse_args()

wait_time = args.wait_time

def main():
# make somekind of while loop here
    while(time_since_last_pic < 120):
        remove_old_pics(old_pics)
        select_pics = select_pics()
        push_to_github(selected_pics)
        old_pics = select_pics
        time_since_last_pic = find_time_since_last_pic()
        time.sleep(wait_time)
    clean_up(old_pics)
    return True

def remove_old_pics(old_pics):
    for pic in old_pics:
        subprocess.run(["git", "rm", "--cached", '"{}"'.formt(pic)])
    subprocess.run(["git", "commit", "-m", "'automated picture removal'"])
    subprocess.run(["git", "push", "origin", "main"])
    return True

def find_time_since_last_pic():
    return time_since_last_pic

def select_pics():
    return selected_pics

def push_to_github(select_pics):
    for pic in select_pics:
        subprocess.run(["git", "add", '"{}"'.formt(pic)])
    subprocess.run(["git", "commit", "-m", "'automated picture add'"])
    subprocess.run(["git", "push", "origin", "main"])
    return True

def clean_up():
    remove_old_pics(old_pics)
    subprocess.run(["git", "add", "end_state.pdf"])
    subprocess.run(["git", "commit", "-m", "'automated picture add'"])
    subprocess.run(["git", "push", "origin", "main"])
    return "Krios-watcher has ended."

if __name__ == '__main__':
    main()
