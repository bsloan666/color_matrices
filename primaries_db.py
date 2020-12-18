import os
import re
import sys

def pkeys():
    return ['name','abbr','redx','redy','greenx','greeny','bluex','bluey','whitex','whitey'] 


def csv_to_dictlist(fname):
    handle = open(fname, 'r')
    lines = handle.readlines()
    handle.close()
    keys = pkeys() 
    result = []
    for line in lines[1:]:
        values = re.split(',',line.rstrip())
        entry = {}
        for i, key in enumerate(keys):
            entry[key] = values[i]
        result.append(entry)

    return result

def dictlist_to_csv(dictlist, fname):
    handle = open(fname, "w")
    keys = pkeys()
    handle.write(','.join(keys)+'\n')
    for entry in dictlist:
        for i,key in enumerate(keys):
            if i:
                handle.write(',')
            handle.write(str(entry[key]))
        handle.write('\n')

    handle.close()

def name_to_param_array(name):
    for entry in DB:
        if name == entry['name'] or name == entry['abbr']:
            return [
                [float(entry['redx']), float(entry['redy'])],
                [float(entry['greenx']), float(entry['greeny'])],
                [float(entry['bluex']), float(entry['bluey'])],
                [float(entry['whitex']), float(entry['whitey'])]
            ]

    return None        


DB = csv_to_dictlist('./color_primaries.csv')

if __name__ == "__main__":
    keys = pkeys()
    if len(sys.argv) != 11:
        print("Wrong number of arguments! For shouls be:")
        print("add_colorspace "+" ".join(keys))
        sys.exit(1)

    db = csv_to_dictlist('./color_primaries.csv')
    entry = {} 
    for i,key in enumerate(keys):
        entry[key] = sys.argv[i+1]
    db.append(entry)
    dictlist_to_csv(db, './color_primaries.csv')
    print("Successfully added " + entry['name'] + " color primaries and whitepoint.")
    

