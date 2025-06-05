from pyhive import hive
import pandas as pd
import warnings

warnings.filterwarnings('ignore')


def connect_to_hive():
    try:
        conn = hive.Connection(
            host='192.168.98.101',
            port=10000,
            username='hadoop',
            database='movie_data',
            auth='NOSASL'
        )
        print("Hive连接成功...")
        return conn
    except Exception as e:
        print(f"Hive连接失败: {e}")
        return None


def get_movie_data():
    conn = connect_to_hive()
    if not conn:
        return None

    try:
        # 存储所有查询
        queries = {
            "rating_counts": """  
                SELECT m.title as title, COUNT(*) as rating_count  
                FROM ratings r  
                JOIN movies m ON r.movieId = m.movieId  
                GROUP BY m.title  
                ORDER BY rating_count DESC  
                LIMIT 10  
            """,

            "gender_ratings": """  
                SELECT m.title as title, u.gender as gender, AVG(r.rating) as avg_rating  
                FROM ratings r  
                JOIN movies m ON r.movieId = m.movieId  
                JOIN users u ON r.userId = u.userId  
                GROUP BY m.title, u.gender    
                ORDER BY avg_rating DESC  
                LIMIT 10  
            """,

            "age_ratings": """  
                SELECT   
                    m.title as title,  
                    CASE   
                        WHEN u.age < 18 THEN '0-17'  
                        WHEN u.age BETWEEN 18 AND 24 THEN '18-24'  
                        WHEN u.age BETWEEN 25 AND 34 THEN '25-34'  
                        WHEN u.age BETWEEN 35 AND 44 THEN '35-44'  
                        WHEN u.age BETWEEN 45 AND 54 THEN '45-54'  
                        ELSE '55+'  
                    END AS age_group,  
                    AVG(r.rating) as avg_rating  
                FROM ratings r  
                JOIN movies m ON r.movieId = m.movieId  
                JOIN users u ON r.userId = u.userId  
                WHERE m.movieId = 520  
                GROUP BY m.title,   
                    CASE   
                        WHEN u.age < 18 THEN '0-17'  
                        WHEN u.age BETWEEN 18 AND 24 THEN '18-24'  
                        WHEN u.age BETWEEN 25 AND 34 THEN '25-34'  
                        WHEN u.age BETWEEN 35 AND 44 THEN '35-44'  
                        WHEN u.age BETWEEN 45 AND 54 THEN '45-54'  
                        ELSE '55+'  
                    END  
                ORDER BY age_group  
            """,

            "top_rated": """  
                SELECT m.title as title, AVG(r.rating) as avg_rating  
                FROM ratings r  
                JOIN movies m ON r.movieId = m.movieId  
                GROUP BY m.title    
                ORDER BY avg_rating DESC  
                LIMIT 10  
            """,

            "best_year": """  
                SELECT YEAR(FROM_UNIXTIME(ratings.rating_timestamp)) AS year, movies.title as title, AVG(ratings.rating) AS avg_rating
        FROM ratings
        JOIN movies ON ratings.movieId = movies.movieId
        GROUP BY YEAR(FROM_UNIXTIME(ratings.rating_timestamp)), movies.title
        ORDER BY year DESC, avg_rating DESC
        LIMIT 10  
            """,

            "top_comedy": """  
                SELECT m.title as title, AVG(r.rating) as avg_rating  
                FROM ratings r  
                JOIN movies m ON r.movieId = m.movieId  
                WHERE m.genres LIKE '%Comedy%'  
                GROUP BY m.title    
                ORDER BY avg_rating DESC  
                LIMIT 10  
            """,

            "top_by_genre": """  
                WITH exploded_genres AS (  
                    SELECT   
                        movieId,  
                        title,  
                        genre  
                    FROM movies  
                    LATERAL VIEW explode(split(genres, '\\\\|')) genres_table AS genre
                    WHERE genre != '(no genres listed)'  
                ),  
                genre_rankings AS (  
                    SELECT   
                        eg.genre,  
                        eg.title,  
                        AVG(r.rating) as avg_rating,    
                        ROW_NUMBER() OVER (PARTITION BY eg.genre ORDER BY AVG(r.rating) DESC) as rank  
                    FROM exploded_genres eg  
                    JOIN ratings r ON eg.movieId = r.movieId  
                    GROUP BY eg.genre, eg.title    
                )  
                SELECT genre, title, avg_rating  
                FROM genre_rankings  
                WHERE rank <= 5  
                ORDER BY genre, avg_rating DESC  
            """
        }

        # 执行所有查询并存储结果
        results = {}
        for name, query in queries.items():
            results[name] = pd.read_sql(query, conn)
            print(results[name])

        return results

    except Exception as e:
        print(f"语句错误: {e}")
        return None

    finally:
        conn.close()
        print("连接关闭")
if __name__ == "__main__":
    results = get_movie_data()