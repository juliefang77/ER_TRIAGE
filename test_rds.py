# test_rds.py
import mysql.connector
import socket

def test_connection():
    try:
        host = "rm-2ze2kv4q8gb81njrhro.mysql.rds.aliyuncs.com"
        print(f"1. Testing DNS resolution for {host}")
        ip = socket.gethostbyname(host)
        print(f"2. DNS resolved to IP: {ip}")
        
        print("3. Testing TCP connection to port 3306...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((ip, 3306))
        if result == 0:
            print("4. TCP connection successful!")
        else:
            print(f"4. TCP connection failed with error code: {result}")
        sock.close()
        
        print("5. Attempting MySQL connection...")
        connection = mysql.connector.connect(
            host=host,
            user="jing_ju_database",
            password="Jingzhumiao7&",
            port=3306,
            database="er_triage_production",
            auth_plugin='mysql_native_password'
        )
        
        print("6. Successfully connected to RDS!")
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"7. MySQL version: {version[0]}")
        
        connection.close()
        
    except socket.gaierror as e:
        print(f"DNS resolution error: {e}")
    except socket.error as e:
        print(f"Socket error: {e}")
    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_connection()