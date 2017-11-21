from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import pymysql
import sys

factory = StemmerFactory()
stemmer = factory.create_stemmer()
judul = "Lumpia Semarang Jajanan Khas dari Semarang, Jawa tengah"
url = "http://www.negerikuindonesia.com/2015/05/lumpia-semarang-jajanan-khas-dari.html"
filename = "lumpia.txt"

count = dict()

f = open(filename,"r",encoding='utf-8')
read = f.read()
f2 = open("stopword.txt","r")
stop = f2.read()
# f3 = open("coba2_hasil.txt","w")
coba = read.split()
coba2 = stop.split()
judul_split = judul.split()

for i in judul_split:
    coba.append(i)

for ch in ['”','–','“',"'"]:
    read = read.replace(ch," ")

low = [x.lower() for x in coba]

for i in low:
    word = i
    for ch in ['.',',','!','(',')',';','”','“',']','[',':','?','/','"','-']:
        word = word.replace(ch,"")
        i = word
        
    # print(i)
    terus = "True"
    for j in coba2:
        # print(j)
        if i==j:
            terus = "False"
            break
    
    # print(terus)
    if terus == "True":
        if stemmer.stem(i) in count:
            count[stemmer.stem(i)] +=1
        else:
            count[stemmer.stem(i)] = 1
        # print(stemmer.stem(i))
        # f3.write(stemmer.stem(i)+'\n')


# for key, value in count.items() :
#     print (key, value)
# print(count)

# Open database connection
db = pymysql.connect("localhost","root","","text_mining" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
for key, value in count.items():
    sql = "INSERT INTO text(judul, berita, url, keyword, jumlah) VALUES ('%s', '%s', '%s', '%s', '%d')" % (judul, read, url, key, value)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
        e = sys.exc_info()
        print(e)

# disconnect from server
db.close()