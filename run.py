import mnt.py as mnt

if __name__ == "__main__":
    f = open(sys.argv[1], "r")
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        mnt(line)
    f.close()

