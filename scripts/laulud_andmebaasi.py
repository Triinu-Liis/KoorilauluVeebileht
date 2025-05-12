import pymysql
from urllib.request import urlopen
import re
import json
#import os

DB_HOST = 'triinuliist.mysql.eu.pythonanywhere-services.com'
DB_USER = 'triinuliist'
DB_PASSWORD = 'KoorilauluApp25'
DB_NAME = 'triinuliist$koorilauluapp'

# Connect to the database
connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

cursor = connection.cursor()

# Laul koos kõikide partiidega
kaust_partiid = "https://haalepartiid25.laulupidu.ee/Song/"
# Üksiku partii mp3 failid
kaust_mp3 = "https://haalepartiid25.laulupidu.ee/assets/songs/"

# naiskoori laulud
koorid = ["naiskoor", "meeskoor", "segakoor", "ühendkoor"]
ids = [[71, 72, 108, 95, 59, 62], [94, 80, 81, 43, 60], [75, 109, 110, 70, 44, 58, 61], [117, 77, 69, 74, 111, 96]]
naiskoor = [71, 72, 108, 95, 59, 62]
meeskoor = [94, 80, 81, 43, 60]
segakoor = [75, 109, 110, 70, 44, 58, 61]
ühendkoor = [117, 77, 69, 74, 111, 96]


cursor.execute("CREATE TABLE IF NOT EXISTS Partiid (id INT NOT NULL AUTO_INCREMENT,Nimi VARCHAR(255) NOT NULL,Partii VARCHAR(255) NOT NULL,LauluId INT NOT NULL,URL VARCHAR(255) NOT NULL,PartiiId INT NOT NULL,Koor VARCHAR(255),PRIMARY KEY (id));")
cursor.execute("CREATE TABLE IF NOT EXISTS Taktid (id INT NOT NULL AUTO_INCREMENT, Takt VARCHAR(255) NOT NULL, Algus INT NOT NULL, LauluId INT, PRIMARY KEY (id), FOREIGN KEY (LauluId) REFERENCES Partiid(id));")

for koori_ids in range(len(ids)): # [naiskoorIDs, meeskoorIDs...]
    koor = koorid[koori_ids] # mis kooriga on tegu
    for id in ids[koori_ids]: # käime läbi selle koori id-d
        fail = kaust_partiid + str(id) # fail, kus on kirjas pealkiri ja id
        with urlopen(fail) as f:
            sisu = f.read().decode('utf-8')
            #print(sisu)
        pealkiri = re.findall('<h4>.*</h4>', sisu)[0][4:-5]
        pealkiri = re.sub(" ", "_", pealkiri).upper();
        trackid = re.findall('var tracks = .*;', sisu)[0][13:-1]
        track_sisu_json = json.loads(trackid)
        for j in track_sisu_json:
            #print(j)
            partii_nimi = j['name'].upper()
            partii_nimi = re.sub("kõik", "koos", j['name'].upper())
            partii_nimi = re.sub(" ", "_", partii_nimi)
            partii_fail = j['id']
            laulu_url = kaust_mp3 + str(id) + "/" + str(partii_fail) + ".webm"
            cursor.execute("SELECT * FROM Partiid where partiiId = %s", partii_fail)
            check = cursor.fetchall()
            if(len(check) == 0):
                cursor.execute("INSERT INTO Partiid(Nimi, Partii, LauluId, PartiiId, URL, Koor) values (%s, %s, %s, %s, %s, %s)", (pealkiri, partii_nimi, id, partii_fail, laulu_url, koor))
                cursor.execute("SELECT * from Partiid where Nimi=%s", pealkiri)
                print(cursor.fetchall())
        bookmarkid = re.findall('var bookmarks = .*;', sisu)[0][16:-1]
        bookmark_sisu_json = json.loads(bookmarkid)

        # Lisan takti märgised andmebaasi
        for b in bookmark_sisu_json:
            takt = b['name']
            algus = b['time']
            laulu_id = b['songId']
            cursor.execute('SELECT id FROM Partiid where LauluId=%s', laulu_id)
            partii_id = cursor.fetchall()
            for id in partii_id:
                cursor.execute('SELECT algus FROM Taktid where LauluId=%s', id)
                kas_leidub_takt = cursor.fetchall()
                if(kas_leidub_takt != algus):
                    print("Lisan takti laulu")
                    print(id)
                    cursor.execute("INSERT INTO Taktid(Takt, Algus, LauluId) values (%s, %s, %s)", (takt, algus, id))


connection.commit()
# Close the connection
cursor.close()
connection.close()