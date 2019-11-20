import argparse
import certifi
import json
import sys
import urllib3


def __construct_parser():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument("-b", nargs=1, dest="board")

    return parser


def __parse():
    parser = __construct_parser()
    args = parser.parse_args(sys.argv[1:])
    return vars(args)


def fetch_board(args):
    thread_url = "https://a.4cdn.org/" + args["board"][0] + "/catalog" + ".json"
    http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
    r = http.request("GET", thread_url)
    return json.loads(r.data.decode("utf-8"))


def gather_ops(board):
    for page in board:
        for thread in page["threads"]:
            if "sub" in thread:
                print(
                    "Thread",
                    str(thread["no"]) + ":\t",
                    thread["sub"] + "(" + str(thread["images"]) + " images)",
                )
            else:
                print(
                    "Thread",
                    str(thread["no"])
                    + ":\t no subject ("
                    + str(thread["images"])
                    + " images)",
                )


def main():
    args = __parse()
    thread = fetch_board(args)
    gather_ops(thread)


if __name__ == "__main__":
    main()
