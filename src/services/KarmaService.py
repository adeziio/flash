import os
from cryptography.fernet import Fernet
from boto3.dynamodb.conditions import Attr
from datetime import date
from dotenv import load_dotenv, find_dotenv
from ..controllers import AWSController

load_dotenv(find_dotenv())

key = bytes(os.getenv("USER_CRYPTO_KEY"), encoding='utf-8')
fernet = Fernet(key)

current_year = str(date.today().year)

def hasEntry(id):
    ret = False
    try:
        response = AWSController.KarmaController.scan(
            FilterExpression=Attr('id').eq(id) & Attr('karma_year').eq(current_year)
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
        id = f'{str(userId)}-{str(serverId)}'
        if (not hasEntry(id)):
            point = 0
            if (sentiment == 'positive'):
                point += 1
            elif (sentiment == 'negative'):
                point -= 1
            try:
                AWSController.KarmaController.put_item(
                    Item={
                        'id': id,
                        'karma_year':current_year,
                        'karma_point': point
                    }
                )
            except Exception as e:
                ret = "Error"
                print(e)
        else:
            point = getPoint(id)
            if (sentiment == 'positive'):
                point += 1
            elif (sentiment == 'negative'):
                point -= 1
            try:
                AWSController.KarmaController.update_item(
                    Key={
                        'id': id
                    },
                    UpdateExpression="SET karma_point = :kpoint",
                    ConditionExpression="karma_year =:kyear",
                    ExpressionAttributeValues={
                        ":kpoint": point,
                        ":kyear": current_year,
                    },
                )
            except Exception as e:
                ret = "Error"
                print(e)
    return ret


def getPoint(id):
    point = 0
    try:
        response = AWSController.KarmaController.scan(
            FilterExpression=Attr('id').eq(id) & Attr('karma_year').eq(current_year)
        )
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                point =  int(response['Items'][0]['karma_point'])
    except Exception as e:
        print(e)
    return point

def getRanking(serverId, karmaYear):
    data = []
    karmaYear = karmaYear if (karmaYear is not None and karmaYear != "") else current_year
    try:
        response = AWSController.KarmaController.scan(
            FilterExpression=Attr('id').contains(str(serverId)) & Attr('karma_year').eq(karmaYear)
        )
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                data =  response['Items']
    except Exception as e:
        print(e)
    return data