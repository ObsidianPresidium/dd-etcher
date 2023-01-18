# sudo pip install prettytable file-explorer
from subprocess import run
from prettytable import PrettyTable
from pick import pick
import os
import sys
from getopt import getopt


parsed_image_file = ""
asked_for_help = False
def parseargs():
    opts, args = getopt(sys.argv[1:], "hi:", ["--help"])
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            global asked_for_help
            asked_for_help = True
            print("Usage: dd-etcher [-i image_file]")
            print("Etch a disk image to a disk.")
        elif opt == "-i":
            global parsed_image_file
            parsed_image_file = os.path.abspath(arg)

def pick_file():
    file_picked = False
    while not file_picked:
        list = [".."]
        list = list + sorted(os.listdir("."))
        enum = 0
        while enum < len(list):
            item = list[enum]
            if not os.path.isdir(item):
                extension = (os.path.splitext(item))[1]
                if extension != ".iso":
                    list.pop(enum)
                    enum -= 1
            enum += 1
        selected_file = pick(list, f"Select image file to be written\n{os.getcwd()}>")
        if selected_file[0] == "..":
            os.chdir("..")
        elif os.path.isdir(os.path.abspath(selected_file[0])):
            os.chdir(os.path.abspath(selected_file[0]))
        else:
            file_picked = True
    return os.path.abspath(selected_file[0])


def get_disks():
    disks_raw = run("lsblk -dro NAME,SIZE,MODEL,RM", capture_output=True, shell=True).stdout
    disks_raw = str(disks_raw, "utf-8")
    # print(disks_raw)
    disks_raw = disks_raw.split("\n")
    # print(len(disks_raw))
    disks_raw.pop(0)
    disks_raw.pop(len(disks_raw) - 1)
    # TODO: Find a different solution. This is non-pythonic
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
    if parsed_image_file == "":
        image_file = pick_file()
    else:
        image_file = parsed_image_file
    print(image_file)
    disks = get_disks()
    # TODO: Turn this into a pick call
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

parseargs()
if not asked_for_help:
    dd_etcher()