import time
import os
import sys
import socket
import shutil
from envs.cityflow_env import CityFlowEnv
from utils.arguments import parse_args
from utils.log import log, loginit, logexit


def main_wrapper(args):
    args = vars(parse_args(args))
    args = loginit(args)
    log(args, level="ALL")
    M = args["main"]


def main_wrapper(args):
    args = vars(parse_args(args))
    args = loginit(args)
    log(args, level="ALL")
    M = args["main"]

    def cleancheck(args):
        clean_flag = False
        if args["clean_logs"]:
            clean_flag = True
            if not args["force_clean"]:
                log(
                    "run over, try to clean log folder `%s`. are you sure to "
                    "clean? if not, press Ctrl+C" % args["log_folder"]
                )
                try:
                    input()
                except KeyboardInterrupt:
                    clean_flag = False
                except EOFError:
                    log("got EOF, stop cleaning", level="WARN")
                    clean_flag = False
        lf = os.path.split(args["log_folder"])
        if len(lf[1]) == 0:  # last folder name not split
            lf = os.path.split(lf[0])
        assert len(lf[1]) != 0
        lf = lf[1]
        os.makedirs("./results/cleaned", exist_ok=True)
        srcfile = "%s/main.log" % args["log_folder"]
        destfile = "./results/%s%s_%s.log" % (
            "cleaned/" if clean_flag else "",
            lf,
            socket.gethostname(),
        )
        open(destfile, "w").write(open(srcfile).read())
        if clean_flag:
            logexit()
            if "linux" in sys.platform:
                os.system("rm -r %s" % args["log_folder"])
            else:
                print(
                    "[ERROR] not in linux, cannot remove log folder! please "
                    "remove it manually."
                )

    cleancheck(args)
    done = False
    env = CityFlowEnv(args["log_folder"], args["work_folder"], args["cityflow_config"])
    print(env.action_space)
    while not done:
        obs, rew, done, info = env.step(env.action_space.sample())
        print(info["average_delay"])
        print(rew)


if __name__ == "__main__":
    main_wrapper(sys.argv)
