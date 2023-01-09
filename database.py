import os
import pymysql

from datetime import date

current_year = str(date.today().year)


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
            AND karma_year='{current_year}'
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
                AND karma_year='{current_year}'
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
                VALUES ('{userId}', '{serverId}', '{current_year}', {karma_point})
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
        AND karma_year='{current_year}'
    '''

    if (cursor.execute(sql) == 1):
        data = cursor.fetchall()
        karma_point = int(data[0][0])
    db.close()
    return karma_point


def select_karma_ranking(serverId, year):
    data = []
    db, cursor = connect()

    k_year = year if (year is not None and year != "") else current_year
    sql = f'''
        SELECT * 
        FROM yoshii.karma
        WHERE server_id='{serverId}'
        AND karma_year='{k_year}'
        ORDER BY karma_point desc
    '''

    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    return data
