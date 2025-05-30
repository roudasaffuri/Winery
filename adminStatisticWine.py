from db_connection import create_connection, disconnection
from datetime import datetime

def statisticWine(wine_id):
    labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    dt = datetime.now()
    thisYear = dt.year
    lastYear = thisYear - 1

    monthsOfThisYear = [0] * 12
    monthsOfLastYear = [0] * 12

    conn = create_connection()
    cursor = conn.cursor()

    sql = "SELECT * FROM wines WHERE id = %s;"
    cursor.execute(sql, (wine_id,))
    result = cursor.fetchone()


    sql = "SELECT * FROM purchase_items WHERE wine_id = %s;"
    cursor.execute(sql, (wine_id,))
    result = cursor.fetchall()
    discount = result[9]


    for row in result :
        purchase_id = row[1]
        sql = "SELECT * FROM purchases WHERE purchase_id = %s;"
        cursor.execute(sql, (purchase_id,))
        result = cursor.fetchone()
        # print(result[5]) # time ==>  2025-05-24 15:00:22.143595 ==> to get just the year 2025
        yearOfPurchase = int((str(result[5]))[:4])
        monthOfPurchase = int((str(result[5]))[5:7]) #  ==> to get just the month
        if yearOfPurchase == thisYear:
            monthsOfThisYear[monthOfPurchase-1] += int(row[4])

        elif yearOfPurchase == lastYear:
            monthsOfLastYear[monthOfPurchase-1] += int(row[4])




    n = len(monthsOfLastYear)
    sum_x = sum(monthsOfLastYear)
    sum_x_squared = sum(x ** 2 for x in monthsOfLastYear)

    variance = (sum_x_squared - (sum_x ** 2) / n) / (n - 1)
    std_dev = variance ** 0.5
    media = (sum_x/12)

    disconnection(conn,cursor)
    return labels, monthsOfThisYear, monthsOfLastYear, std_dev, media ,discount


