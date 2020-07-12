import bs4 as bs
from urllib.request import Request, urlopen
import time
import webbrowser

def archive(path, *args):
    try:
        file = open(path, "r")
    except:
        print("file not found")
        return
    text = ""

    for line in file.readlines():
        line = line[:-1]
        line += " " * (80 - (len(line) % 80))
        text += line

    text = text.replace(" ", "+")
    soup = bs.BeautifulSoup(urlopen(Request(f"https://libraryofbabel.info/search.cgi?find={text}&btnSubmit=Search&method=x",headers={'User-Agent': 'Mozilla/5.0'})), "lxml")
    
    if args:
        outputfile = open(args[0], "w")
    else:
        tm = time.localtime()
        outputfile = open(f"{tm.tm_sec}s{tm.tm_min}m{tm.tm_hour}h{tm.tm_mday}d{tm.tm_mon}m{tm.tm_year}y.txt", "w")
        
    outputfile.write(soup.a["onclick"][9:-1])
    outputfile.close()
    print("successfully archived.")

def find(path):
    file = open(path, "r")
    arr = file.read().split(",")
    file.close()
    
    for i in range(len(arr)):
        arr[i] = arr[i][1:-1]

    try:
        file = open("config.txt", "r")
        browser = file.readlines()[0]
        browser_path = file.readlines()[1]
        webbrowser.register(browser, None,webbrowser.BackgroundBrowser(browser_path))
        webbrowser.get(browser).open_new_tab(f"https://libraryofbabel.info/book.cgi?{arr[0]}-w{arr[1]}-s{arr[2]}-v{arr[3]}:{arr[4]}")
    except:
        webbrowser.open(f"https://libraryofbabel.info/book.cgi?{arr[0]}-w{arr[1]}-s{arr[2]}-v{arr[3]}:{arr[4]}")
    print("finding in browser...")

#def setBrowser(browser, path):
#    file = open("config.txt", "w")
#    file.write(f"{browser}\n{path}")
#    file.close()
    

running = True

print("Started, please enter command\n")

while running:
    action = input(":").split(" ")

    if action[0] == "archive":
        if len(action) == 3:
            archive(action[1], action[2])
        elif len(action) == 2:
            archive(action[1])
        else:
            print("invalid command\n\ntype \"help\" for instructions")
    elif action[0] == "find":
        if len(action) == 2:
            find(action[1])
        else:
            print("invalid command\n\ntype \"help\" for instructions")
    elif action[0] == "help":
        print("----------------------------------------------------------------------------------------\nPlease use the following commands:\n\narchive       [path of text file] [path of output archive file] default: date + time\nfind          [path of archive file]\nquit or exit")
    elif action[0] == "quit" or action[0] == "exit":
        running = False
    #elif action[0] == registerBrowser and len(action) == 3:
    #    setBrowser(action[1], action[2])   
    else:
        print("invalid command\n\ntype \"help\" for instructions")
