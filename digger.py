import twitter
from typing import List


class Digger:
    def __init__(self, consumerToken, consumerTokenSecret, accessToken, accessTokenSecret):
        self.api = twitter.api.Api(
            consumer_key=consumerToken,
            consumer_secret=consumerTokenSecret,
            access_token_key=accessToken,
            access_token_secret=accessTokenSecret,
            sleep_on_rate_limit=True
        )

    def getFollowerIDs(self, screenName: str, cursor=-1):
        nextCursor, preCursor, result = self.api.GetFollowerIDsPaged(
            screen_name=screenName,
            cursor=cursor,
            count=5000
        )
        return nextCursor, preCursor, result

    def getUserDetails(self, userIDs):
        return self.api.UsersLookup(user_id=userIDs)
