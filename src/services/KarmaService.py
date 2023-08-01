import os
from datetime import datetime
from cryptography.fernet import Fernet
from boto3.dynamodb.conditions import Attr
from datetime import date
from dotenv import load_dotenv, find_dotenv
from ..controllers import AWSController

load_dotenv(find_dotenv())

key = bytes(os.getenv("USER_CRYPTO_KEY"), encoding='utf-8')
fernet = Fernet(key)

current_year = str(date.today().year)

def hasEntry(userId, serverId):
    ret = False
    try:
        response = AWSController.KarmaController.scan(
            FilterExpression=Attr('user_id').eq(userId) and Attr('server_id').eq(serverId) and Attr('year').eq(current_year)
        )
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                data =  response['Items']
                if (len(data) > 0):
                    ret = True
    except Exception:
        ret = False
    return ret

def addPoint(userId, serverId, sentiment):
    ret = "Success"
    if (sentiment == 'positive' or sentiment == 'negative'):
        if (not hasEntry(userId, serverId)):
            point = 0
            if (sentiment == 'positive'):
                point += 1
            elif (sentiment == 'negative'):
                point -= 1
            try:
                AWSController.KarmaController.put_item(
                    Item={
                        'user_id': userId,
                        'server_id': serverId,
                        'year':current_year,
                        'point': point
                    }
                )
            except Exception as e:
                ret = "Error"
                print(e)
        else:
            point = getPoint(userId, serverId)
            if (sentiment == 'positive'):
                point += 1
            elif (sentiment == 'negative'):
                point -= 1
            try:
                AWSController.KarmaController.update_item(
                    Key={
                        'user_id': userId
                    },
                    UpdateExpression="SET point = :point",
                    ExpressionAttributeValues={
                        ":point": point,
                    },
                )
            except Exception as e:
                ret = "Error"
                print(e)
    return ret


def getPoint(userId, serverId):
    point = 0
    try:
        response = AWSController.KarmaController.scan(
            FilterExpression=Attr('user_id').eq(userId) and Attr('server_id').eq(serverId) and Attr('year').eq(current_year)
        )
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                point =  int(response['Items'][0]['point'])
    except Exception as e:
        print(e)
    return point

def getRanking(serverId, year):
    data = []
    year = year if (year is not None and year != "") else current_year
    try:
        response = AWSController.KarmaController.scan(
            FilterExpression=Attr('server_id').eq(serverId) and Attr('year').eq(year)
        )
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                data =  response['Items']
    except Exception as e:
        print(e)
    return data