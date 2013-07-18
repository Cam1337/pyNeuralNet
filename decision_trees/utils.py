def chunks(l, n):
    """
    Yield successive n-sized chunks from l.
    http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    """
    results = []
    for i in xrange(0, len(l), n):
        results.append( l[i:i+n] )
    return results

def shavexy(l, x, y):
    l = l[y:]
    l = [i[x:] for i in l]
    return l

def shavewh(l, w, h):
    l = l[:h]
    l = [i[:w] for i in l]
    return l