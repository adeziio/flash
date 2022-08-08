import os
import pymysql

db = None
cursor = None


def initialize_db():
    global db
    global cursor

    db = pymysql.connect(
        host=os.getenv('AWS_RDS_HOST'), user=os.getenv('AWS_RDS_USER'), password=os.getenv('AWS_RDS_PASS'))
    cursor = db.cursor()


def update_karma(userId, userName, serverId, serverName,
                 userNameInServer, sentiment):
    global db
    global cursor

    # check if row already exists in database
    sql = f'''
        SELECT * 
        FROM yoshii.karma
        WHERE user_id='{userId}'
        AND user_name='{userName}'
        AND server_id='{serverId}'
        AND server_name='{serverName}'
        AND user_name_in_server='{userNameInServer}'
    '''

    # if row exist in database, update
    if (cursor.execute(sql) == 1):
        data = cursor.fetchall()
        new_karma = int(data[0][6])
        if (sentiment == 'positive'):
            new_karma += 1
        elif (sentiment == 'negative'):
            new_karma -= 1
        else:
            return ""
        sql = f'''
            UPDATE yoshii.karma
            SET karma_point={new_karma}
            WHERE user_id='{userId}'
            AND user_name='{userName}'
            AND server_id='{serverId}'
            AND server_name='{serverName}'
            AND user_name_in_server='{userNameInServer}'
        '''

    # if row does not exist in database, insert
    else:
        new_karma = 0
        if (sentiment == 'positive'):
            new_karma += 1
        elif (sentiment == 'negative'):
            new_karma -= 1
        sql = f'''
            INSERT INTO yoshii.karma
            VALUES (default, '{userId}', '{userName}', '{serverId}', '{serverName}', '{userNameInServer}', {new_karma})
        '''

    # execute and commit
    cursor.execute(sql)
    db.commit()

    return ""
