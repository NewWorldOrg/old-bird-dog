from pathlib import Path
import time
import pandas as pd
import twitter
from typing import List
import logging
import logging.config

logging.config.fileConfig("./logging.conf")


class Writer:
    def __init__(self, dist: str, fileName: str):
        # path complete
        now = time.strftime("%Y%m%d%H%M%S")
        p = Path(dist).absolute()
        if not Path(dist).exists():
            p.mkdir()
        # paths
        self.distPath = p
        self.distFilePath = p / "{}-{}".format(now, fileName)
        logging.info("dist path : {}".format(self.distPath))
        logging.info("dist file path : {}".format(self.distFilePath))
        # dataframe column def
        self.userDfColumns = ["userid", "name", "screen_name", "protected",
                              "follow", "follower", "description","tweet_count", "created_at"]
        self.userIDsDfColumns = ["userid"]

    def toDataFrameFromUser(self, user: twitter.User):
        return pd.DataFrame({
            "userid": [user.id_str],
            "name": [user.name],
            "screen_name": [user.screen_name],
            "protected": [user.protected],
            "follow": [user.friends_count],
            "follower": [user.followers_count],
            "description": [user.description],
            "tweet_count": [user.statuses_count],
            "created_at": [user.created_at]
        }, columns=self.userDfColumns)

    def toDataFrameFromUserID(self, userID):
        return pd.DataFrame({
            "userid": [userID]
        }, columns=self.userIDsDfColumns)

    def saveUserDetailsToCSV(self, users: List[twitter.User] = []):
        df = pd.DataFrame(columns=self.userDfColumns)
        for user in users:
            df = pd.concat([df, self.toDataFrameFromUser(user)], sort=False)
        out = "{}-follower-details.csv".format(str(self.distFilePath))
        if Path(out).exists():
            df.to_csv(out, index=False, header=False, mode='a')
        else:
            df.to_csv(out, index=False, mode='w')
        logging.info("saved : {}".format(out))

    def saveUserIDsToCSV(self, userIDs=[]):
        df = pd.DataFrame(columns=self.userIDsDfColumns)
        for userId in userIDs:
            df = pd.concat(
                [df, self.toDataFrameFromUserID(userId)], sort=False)
        out = "{}-follower-ids.csv".format(str(self.distFilePath))
        if Path(out).exists():
            df.to_csv(out, index=False, header=False, mode='a')
        else:
            df.to_csv(out, index=False, mode='w')
        logging.info("saved : {}".format(out))
