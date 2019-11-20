import argparse
import certifi
import json
import os
import sys
import urllib3

"""
Usage:
    python3 ChreadRip.py -b wg -t 7383498 -p ~/Images/ChreadRip/SpringPapes
"""


def __construct_parser():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument("-b", nargs=1, dest="board")
    parser.add_argument("-t", nargs=1, dest="thread")
    parser.add_argument("-p", nargs=1, dest="path")

    return parser


def __parse():
    parser = __construct_parser()
    args = parser.parse_args(sys.argv[1:])
    return vars(args)


def fetch_thread(args):
    thread_url = (
        "https://a.4cdn.org/"
        + args["board"][0]
        + "/thread/"
        + args["thread"][0]
        + ".json"
    )
    http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
    r = http.request("GET", thread_url)
    return json.loads(r.data.decode("utf-8"))["posts"]


def rip_images(thread, path):
    http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())

    for post in thread:
        if "tim" in post:
            file_url = "https://i.4cdn.org/wg/" + str(post["tim"]) + str(post["ext"])
            file_name = file_url.split("/")[-1]

            if not os.path.exists(path + "/" + file_name):
                r = http.request("GET", file_url, preload_content=False)

                meta = r.info()
                file_size = int(meta.getheaders("Content-Length")[0])
                print("Downloading: %s Bytes: %s" % (file_name, file_size))

                with open(path + "/" + file_name, "wb") as out:
                    while True:
                        data = r.read()
                        if not data:
                            break
                        out.write(data)

                r.release_conn()


def main():
    """
    Downloads every file form 4chan thread.

    Parameters
    ----------
    -b : board
        4chan Board ID
    -t : thread
        Thread number
    -p : path
        Path on computer for thread folder
    """

    args = __parse()
    thread = fetch_thread(args)

    # Check if path exists
    if not os.path.exists(args["path"][0]):
        os.makedirs(args["path"][0])

    rip_images(thread, args["path"][0])


main()
