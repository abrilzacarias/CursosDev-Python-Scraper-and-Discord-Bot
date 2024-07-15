from datetime import datetime, timedelta
from config import connection

def searchCourses(searchTerm):
    try:
        with connection.cursor() as cursor:
            todayDate = datetime.now().strftime('%Y-%m-%d')

            sql = "SELECT name, creator, url FROM courses WHERE name LIKE %s AND DATE(date) = %s"
            cursor.execute(sql, (f'%{searchTerm}%', todayDate))
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(e)
        return []
    
def getTodayCourses():
    try:
        with connection.cursor() as cursor:
            todayDate = datetime.now().strftime('%Y-%m-%d')

            # Usar DATE() para comparar solo la parte de la fecha
            sql = "SELECT name, creator, url FROM courses WHERE DATE(date) = %s"
            cursor.execute(sql, (todayDate,))
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(e)
        return []

def deleteOldCourses():
    try:
        with connection.cursor() as cursor:
            weekAgo = datetime.now() - timedelta(weeks=1)
            weekAgoStr = weekAgo.strftime('%Y-%m-%d %H:%M:%S')
            sql = "DELETE FROM courses WHERE DATE(date) < %s"
            cursor.execute(sql, (weekAgoStr,))
            connection.commit()
            print(f"Deleted courses scraped more than a week ago ({weekAgoStr})")
    except Exception as e:
        print(e)

def searchCoursesByCreator(creator):
    todayDate = datetime.now().date()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT name, creator, url FROM courses WHERE creator LIKE %s AND DATE(date) = %s"
            cursor.execute(sql, (f'%{creator}%', todayDate))
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"Error: {e}")
        return []