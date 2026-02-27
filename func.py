import requests

from bs4 import BeautifulSoup as BS

def new_coins(val):
    return val * 4 + 1

def new_exp(val):
    return val * 2 + 1

def new_level(val):
    return val * (val - 1) + 2

def get_time(val):
    h = val // 3600
    val -= h * 3600
    m = val // 60
    val -= m * 60
    s = val
    return h, m, s

def update_coins(diff):
    total_coins = new_coins(diff)
    return total_coins

def IsSolvedProblem(problemset, task_id):
    if task_id in problemset:
        return True
    return False

def update_level(diff, exp, level, x):
    exp += new_exp(diff) * x
    while new_level(level) <= exp:
        exp -= new_level(level)
        level += 1
    return new_exp(diff) * x, exp, level

def check_name(name):
    url = "https://codeforces.com/profile/" + name
    html = requests.get(url)
    soup = BS(html.text, "html.parser")
    res = soup.find("div", class_="userbox")
    if res != None:
        return True
    return False

def parser_solves(url, name, task_id):
    html = requests.get(url)
    if html.status_code == 403:
        return False
    soup = BS(html.text, "html.parser")
    res1 = soup.find("span", class_="verdict-accepted")
    all_links = soup.find("div", class_="datatable")
    all_links = all_links.find_all('a')
    res2 = False
    res3 = False
    for link in all_links:
        if task_id in link:
            res3 = True
        if name in link['href']:
            res2 = True
    if res1 == None or res2 is False or res3 is False:
        return False
    return True

def parser_problems(url):
    html = requests.get(url)
    if html.status_code == 403:
        return 0
    soup = BS(html.text, "html.parser")
    all_links = soup.find("div", class_="datatable")
    all_links = all_links.find_all('a')
    task_links = []
    for link in all_links:
        a = "/problem/" in link['href']
        b = "status" in link['href']
        if a is True and b is False:
            task_links.append(link['href'])
    return task_links
