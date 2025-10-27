with open("pitcode.txt", 'a') as fisier:
    for number in range(100):
        fisier.write(f"{number}\n")

fisier.close()