import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv


load_dotenv()
queries = {"total":"""
            SELECT COUNT(*) FROM qr_requests
            """,
    "color":"""
            SELECT COUNT(*) FROM qr_requests 
            WHERE has_color = TRUE
            """,
    "logo" : """
            SELECT COUNT(*) FROM qr_requests 
            WHERE has_logo = TRUE
            """,
    "both": """
            SELECT COUNT(*) FROM qr_requests 
            WHERE has_logo = TRUE AND has_color = TRUE
            """,
    "avg_size" : """
            SELECT AVG(size) FROM public.qr_requests
            """,
    "avg_response" : """
            SELECT AVG(response_time_ms) FROM public.qr_requests
            """
    
}

def get_db_connection():
    """Create and return a database connection"""
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn

def save_qr_analytics(has_color, has_logo, size, response_time_ms):
    count=0
    """Save QR generation analytics to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO qr_requests (has_color, has_logo, size, response_time_ms)
        VALUES (%s, %s, %s, %s)
        """, (has_color, has_logo, size, response_time_ms))
    
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_total_count():
    """Get total number of QR codes generated"""
    count=-1
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT COUNT(*) FROM qr_requests
            """)
        count = cursor.fetchone()[0]
    finally:
        cursor.close()
        conn.close()
    return count
    
def get_count_by_period(timeframe) -> int | None:
    """Get count for a specific time period"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Build SQL query based on timeframe
        if timeframe == "today":
            query = """
                SELECT COUNT(*) FROM qr_requests 
                WHERE created_at >= CURRENT_DATE
            """
        elif timeframe == "month":
            query = """
                SELECT COUNT(*) FROM qr_requests 
                WHERE created_at >= NOW() - INTERVAL '30 days'
            """
        elif timeframe == "year":
            query = """
                SELECT COUNT(*) FROM qr_requests 
                WHERE created_at >= NOW() - INTERVAL '1 year'
            """
        else:
            return None  # Invalid timeframe
        
        cursor.execute(query)
        count = cursor.fetchone()[0]
        return count
        
    finally:
        cursor.close()
        conn.close()


def get_feature_stats()-> dict[float]| None:
    """Get breakdown of feature usage"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(queries["total"])
        total = cursor.fetchone()[0]
        cursor.execute(queries["color"])
        with_color = cursor.fetchone()[0]
        cursor.execute(queries["logo"])
        with_logo = cursor.fetchone()[0]
        cursor.execute(queries["both"])
        with_both = cursor.fetchone()[0]
        cursor.execute(queries["avg_size"])
        average_size = cursor.fetchone()[0]
        cursor.execute(queries["avg_response"])
        average_response_time_ms = cursor.fetchone()[0]
        
        return {"total":total ,"with_color": with_color,
            "with_logo":with_logo,"with_both":with_both,
             "average_size":average_size,
              "average_response_time_ms":average_response_time_ms}
    finally:
        cursor.close()
        conn.close()
        
    
    
    
    
