from db_connection import create_connection


def genderDistribution():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT gender, COUNT(*) FROM users GROUP BY gender")
    results = cursor.fetchall()

    male_count = 0
    female_count = 0

    for gender, count in results:
        if gender == 'Male':
            male_count = count
        elif gender == 'Female':
            female_count = count

    return [male_count, female_count]

