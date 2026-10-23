import json
import os
import pymysql

# RDS Bağlantı Bilgileri (Çevre Değişkenlerinden Alınır)
RDS_HOST = os.environ.get('DB_HOST')
RDS_USER = os.environ.get('DB_USER')
RDS_PASSWORD = os.environ.get('DB_PASSWORD')
RDS_NAME = os.environ.get('DB_NAME')
RDS_PORT = int(os.environ.get('DB_PORT', 3306))

def get_connection():
    return pymysql.connect(
        host=RDS_HOST,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_NAME,
        port=RDS_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    phone_number VARCHAR(50) NOT NULL
                )
            """)
        conn.commit()
        conn.close()
    except Exception as e:
        print("Tablo oluşturma hatası:", str(e))



def lambda_handler(event, context):
    
    init_db()

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }

    # CORS Preflight (OPTIONS) isteği için yanıt
    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return {"statusCode": 200, "headers": headers, "body": ""}

    try:
        # HTTP Metodunu yakala (GET veya POST)
        method = event.get('requestContext', {}).get('http', {}).get('method') or event.get('httpMethod')
        
        connection = get_connection()
        
        # 1. KAYIT EKLEME (POST İsteği)
        if method == 'POST':
            body = json.loads(event.get('body', '{}'))
            name = body.get('name')
            phone_number = body.get('phone_number')

            if not name or not phone_number:
                return {
                    "statusCode": 400,
                    "headers": headers,
                    "body": json.dumps({"message": "İsim ve telefon numarası zorunludur."})
                }

            with connection.cursor() as cursor:
                sql = "INSERT INTO contacts (name, phone_number) VALUES (%s, %s)"
                cursor.execute(sql, (name, phone_number))
                connection.commit()
            
            connection.close()
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({"message": "Kayıt başarıyla eklendi!"})
            }

        # 2. KAYITLARI SORGULAMA / LİSTELEME (GET İsteği)
        elif method == 'GET':
            query_params = event.get('queryStringParameters') or {}
            search_query = query_params.get('search', '')

            with connection.cursor() as cursor:
                if search_query:
                    sql = "SELECT * FROM contacts WHERE name LIKE %s OR phone_number LIKE %s"
                    cursor.execute(sql, (f"%{search_query}%", f"%{search_query}%"))
                else:
                    sql = "SELECT * FROM contacts ORDER BY id DESC LIMIT 50"
                    cursor.execute(sql)
                
                result = cursor.fetchall()

            connection.close()
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({"data": result}, default=str)
            }

        else:
            return {
                "statusCode": 405,
                "headers": headers,
                "body": json.dumps({"message": "Desteklenmeyen HTTP Metodu"})
            }

    except Exception as e:
        print("Hata:", str(e))
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"message": "Veritabanı hatası", "error": str(e)})
        }