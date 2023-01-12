from subprocess import run
from prettytable import PrettyTable


def get_disks():
    disks_raw = run("lsblk -dro NAME,SIZE,MODEL,RM", capture_output=True, shell=True).stdout
    disks_raw = str(disks_raw, "utf-8")
    # print(disks_raw)
    disks_raw = disks_raw.split("\n")
    # print(len(disks_raw))
    disks_raw.pop(0)
    disks_raw.pop(len(disks_raw) - 1)
    # This is non-pythonic. Need to find a different solution
    i = 0
    while i < len(disks_raw):
        if "loop" in disks_raw[i]:
            # print(f"popping {disks_raw[i]}")
            disks_raw.pop(i)
            i -= 1
        i += 1

    for x in enumerate(disks_raw):
        disks_raw[x[0]] = f"/dev/{x[1]}"
        disks_raw[x[0]] = disks_raw[x[0]].split(" ")

    for x in enumerate(disks_raw):
        disks_raw[x[0]][2] = disks_raw[x[0]][2].replace("\\x20", " ")
        if disks_raw[x[0]][3] == "0":
            disks_raw[x[0]][3] = "No"
        else:
            disks_raw[x[0]][3] = "Yes"
    # print(disks_raw)
    return disks_raw


def pretty_print_disks(disks):
    table = PrettyTable(["Number", "Internal name", "Total size", "Model name", "Is removable"])
    #print(disks)
    for x in enumerate(disks):
        table.add_row([x[0], x[1][0], x[1][1], x[1][2], x[1][3]])

    table.align = "l"
    print(table)


def etch(inputfile, outputdisk, blocksize):
    print("Writing...")
    run(f"sudo dd if={inputfile} of={outputdisk} bs={blocksize} status=progress", shell=True)
    print("Done.")

def dd_etcher():
    image_file = input("Enter path to image file to be written: ")
    disks = get_disks()
    pretty_print_disks(disks)
    identifier = input("Select a number or enter internal name: ")
    if identifier.isnumeric():
        identifier = disks[int(identifier)][0]
    blocksize = input("Enter block size (default: 1M): ")
    if blocksize == "":
        blocksize = "1M"
    while True:
        ask = input(f"Confirm you want to write {image_file} to {identifier}? (This will delete any contents of {identifier}!) (Y/N): ")
        if ask in ["Y", "y"]:
            etch(image_file, identifier, blocksize)
            break
        elif ask in ["N", "n"]:
            print("Abort.")
            exit()
        else:
            print(f"Unrecognized option {ask}")

dd_etcher()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
