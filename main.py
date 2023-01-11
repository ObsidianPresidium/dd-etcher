from subprocess import run


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
    # print(disks_raw)
    return disks_raw


def pretty_print_disks(disks):
    for x in enumerate(disks):
        print()


def dd_etcher():
    image_file = input("Enter path to image file to be written: ")
    disks = get_disks()


dd_etcher()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
