import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='cursosdevdb'
)

'''try:
    with connection.cursor() as cursor:
        # Insertar registros
        sql = "INSERT INTO course (name, url, creator) VALUES (%s, %s, %s)"
        cursor.execute(sql, ('Example Site', 'https://www.example.com', 'Example Creator'))
        
        # Confirmar los cambios
        connection.commit()
finally:
    connection.close()'''