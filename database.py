import os
import pymysql


def connect():
    db = pymysql.connect(
        host=os.getenv('AWS_RDS_HOST'), user=os.getenv('AWS_RDS_USER'), password=os.getenv('AWS_RDS_PASS'))
    cursor = db.cursor()
    return db, cursor


def update_karma_point(userId, serverId, sentiment):
    if (sentiment == 'positive' or sentiment == 'negative'):
        db, cursor = connect()

        # check if row already exists in database
        sql = f'''
            SELECT karma_point 
            FROM yoshii.karma
            WHERE user_id='{userId}'
            AND server_id='{serverId}'
        '''

        # if row exist in database, update
        if (cursor.execute(sql) == 1):
            data = cursor.fetchall()
            karma_point = int(data[0][0])
            if (sentiment == 'positive'):
                karma_point += 1
            elif (sentiment == 'negative'):
                karma_point -= 1
            sql = f'''
                UPDATE yoshii.karma
                SET karma_point={karma_point}
                WHERE user_id='{userId}'
                AND server_id='{serverId}'
            '''

        # if row does not exist in database, insert
        else:
            karma_point = 0
            if (sentiment == 'positive'):
                karma_point += 1
            elif (sentiment == 'negative'):
                karma_point -= 1
            sql = f'''
                INSERT INTO yoshii.karma
                VALUES ('{userId}', '{serverId}', {karma_point})
            '''

        # execute and commit
        cursor.execute(sql)
        db.commit()
        db.close()
    return ""


def select_karma_point(userId, serverId):
    karma_point = 0
    db, cursor = connect()

    sql = f'''
        SELECT karma_point 
        FROM yoshii.karma
        WHERE user_id='{userId}'
        AND server_id='{serverId}'
    '''

    if (cursor.execute(sql) == 1):
        data = cursor.fetchall()
        karma_point = int(data[0][0])
    db.close()
    return karma_point
