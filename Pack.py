import struct


def enURL(urls):
    resp = ""
    for url in urls:
        urlsize = len(url.encode("gb2312"))
        resp += str(urlsize) + "s"
    args = []
    for url in urls:
        args.append(url.encode("gb2312"))

    return struct.pack(resp, *args), resp

def deURL(resp, packres):
    finalRt = struct.unpack(resp, packres)
    urls = []
    for url in finalRt:
        urls.append(url.decode("gb2312"))
    return urls

def enURLandWeight(urlS):
    resp = ""
    for urlmark in urlS:
        urlsize = len(urlmark[0].encode("gb2312"))
        resp += str(urlsize) + "s"
        weightsize = len(str(urlmark[1]))
        resp += str(weightsize) + "s"

    args = []
    for urlmark in urlS:
        args.append(urlmark[0].encode("gb2312"))
        args.append(str(urlmark[1]).encode("gb2312"))

    return struct.pack(resp, *args), resp

def deURLandWeight(resp, packres):
    finalRt = struct.unpack(resp, packres)
    ressize = len(finalRt)
    urls = []
    weight = []
    for i in range(ressize):
        if i%2 == 0:
            urls.append(finalRt[i].decode("gb2312"))
        else:
            weight.append(float(finalRt[i]))
    return urls, weight
    

def main():
    pass

if __name__ == "__main__":
    main()

