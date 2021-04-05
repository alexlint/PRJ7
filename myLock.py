import threading

lock = dict()

l1 = threading.Lock()
l2 = threading.Lock()
l3 = threading.Lock()
l4 = threading.Lock()
l5 = threading.Lock()

lock["urllist"] = l1
lock["wordlist"] = l2
lock["link"] = l3
lock["linkword"] = l4
lock["wordlocation"] = l5 
