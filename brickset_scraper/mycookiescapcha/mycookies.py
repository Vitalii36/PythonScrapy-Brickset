import re

def mycook():
    cookies = open("mycookiescapcha/mycookies.txt")
    s = cookies.read()
    s = re.split(';', s)
    mycookies = {}
    for i in s:
        i = re.split('=', i, 1)
        mycookies.update({i[0]: i[1]})
    cookies.close()
    return(mycookies)