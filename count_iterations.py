if __name__ == '__main__':
    readfile = open("hillclimblog.txt", 'r')
    for line in readfile.readlines():
        if line.split()[0] == "generations":
            pass
        else:
            print(len(line.split(";")[:-1]))
