with open("C:\\Users\\tyler\\Documents\\GitHub\\Page-Replacement-Algorithms-Comparative-Performance-Analysis-for-Modern-Virtual-Memory-Systems-\\twitter.txt", "r") as twitter:
    data = twitter.read()
    data = data.split("\n")
    with open("./data.txt", "w") as file:
        for i in range(10000):
            x = data[i].split("\t")
            file.write(x[0])
            file.write("\n")
            file.write(x[1])
            file.write("\n")
            
