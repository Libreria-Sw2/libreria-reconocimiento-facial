'''
    Description:
    Create your own Login with Facial Recognition.

    Author: AlejandroV
    Version: 1.0
    Video: https://youtu.be/cTSVYwxHn9g
'''
import mysql.connector as db
import json

with open('keys.json') as json_file:
    keys = json.load(json_file)

def convertToBinaryData(filename):
    # Convert digital data to binary format
    try:
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData
    except:
        return 0

def write_file(data, path):
    # Convert binary data to proper format and write it on your computer
    with open(path, 'wb') as file:
        file.write(data)

def registerUser(name, photo):
    id = 0
    try:
        con = db.connect(host=keys["host"], user=keys["user"], password=keys["password"], database=keys["database"])
        cursor = con.cursor()
        sql = "INSERT INTO `user`(name, photo) VALUES (%s,%s)"
        pic = convertToBinaryData(photo)

        if pic:
            cursor.execute(sql, (name, pic))
            con.commit()
            id = cursor.lastrowid
    except db.Error as e:
        print(f"Failed inserting image: {e}")
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
    return {"id": id}

def getUser(name, path):
    id = 0
    rows = 0
    try:
        con = db.connect(host=keys["host"], user=keys["user"], password=keys["password"], database=keys["database"])
        cursor = con.cursor()
        sql = "SELECT * FROM `user` WHERE name = %s"

        cursor.execute(sql, (name,))
        coincidencias = cursor.fetchall()
        for row in coincidencias:
            id = row[0]
            write_file(row[2], path)
        rows = len(coincidencias)
        print("rows",rows)
    except db.Error as e:
        print(f"Failed to read image: {e}")
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
    return {"id": id, "affected": rows}
