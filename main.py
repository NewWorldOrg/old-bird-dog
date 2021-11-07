import argparse
import configparser
import logging
import twitter
import pandas as pd
from typing import List
from queue import Queue
from digger import Digger
from writer import Writer

config = configparser.ConfigParser()
config.read("./config.ini")


class Main:
    def __init__(self, targetUser: str, dist: str, source: str = "", nextCursor=-1):
        # config
        self.configFilePath = "./config.ini"
        self.config = configparser.ConfigParser()
        self.config.read(self.configFilePath)
        # digger
        twitterConf = self.config["Twitter"]
        self.digger = Digger(
            twitterConf["CONSUMER_TOKEN"],
            twitterConf["CONSUMER_TOKEN_SECRET"],
            twitterConf["ACCESS_TOKEN"],
            twitterConf["ACCESS_TOKEN_SECRET"]
        )
        self.nextCursor = nextCursor
        self.targetUser = targetUser
        self.gotCnt = 0
        # writer
        self.writer = Writer(dist, targetUser)
        # reader
        self.source = source

    def getFollowerIDs(self):
        try:
            while self.nextCursor != 0:
                nextCursor, preCursor, result = self.digger.getFollowerIDs(
                    self.targetUser, self.nextCursor)
                self.gotCnt = self.gotCnt + len(result)
                logging.info("got follower ids")
                logging.debug("got ids : \n{}".format(result))
                logging.info("count : {}".format(self.gotCnt))
                logging.info("pre cursor : {}".format(preCursor))
                logging.info("next cursor : {}".format(nextCursor))
                self.nextCursor = nextCursor
                self.writer.saveUserIDsToCSV(result)
        except twitter.error.TwitterError as err:
            logging.error(err)
        except KeyboardInterrupt:
            logging.info("next cursor : {}".format(self.nextCursor))

    def getFollowerDetails(self):
        reader = pd.read_csv(self.source, usecols=[
                             'userid'], dtype='str', chunksize=100)
        try:
            for chunk in reader:
                ids = chunk.values.flatten().tolist()
                details = self.digger.getUserDetails(ids)
                self.gotCnt = self.gotCnt + len(details)
                logging.info("got user details")
                logging.info("count : {}".format(self.gotCnt))
                logging.debug("got user : \n{}".format(ids))
                self.writer.saveUserDetailsToCSV(details)
        except twitter.error.TwitterError as err:
            logging.error(err)
        except KeyboardInterrupt:
            logging.info("stop!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--user", "-u", help="取得したいユーザのスクリーンネーム（@は省略して入力）", type=str, required=True
    )
    parser.add_argument(
        "--source", "-s", help=""
    )
    parser.add_argument(
        "--output", "-o", help="ファイル出力先ディレクトリ (default : \"./output\")", default="./output", type=str
    )
    parser.add_argument(
        "--cursor", "-c", help="(default : -1)", default="-1"
    )
    parser.add_argument(
        "--type", "-t", help="id(IDの収集), detail(ユーザ詳細の収集))", required=True
    )
    args = parser.parse_args()
    if args.type == "id":
        main = Main(args.user, args.output, args.source, args.cursor)
        main.getFollowerIDs()
    elif args.type == "detail":
        if args.source != "":
            main = Main(args.user, args.output, args.source, args.cursor)
            main.getFollowerDetails()
        else:
            logging.error("need set source")
    else:
        logging.error("unknown type (id or detail)")
