from flask import request, render_template

from db_connection import create_connection, disconnection
from datetime import datetime

def viewStatisticByIdWine():
    wine_id = request.form.get('id')

    labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    dt = datetime.now()
    thisYear = dt.year
    lastYear = thisYear - 1

    monthsOfThisYear = [0] * 12
    monthsOfLastYear = [0] * 12

    conn = create_connection()
    cursor = conn.cursor()


    sql = "SELECT * FROM purchase_items WHERE wine_id = %s;"
    cursor.execute(sql, (wine_id,))
    result = cursor.fetchall()


    for row in result :
        purchase_id = row[1]
        sql = "SELECT * FROM purchases WHERE purchase_id = %s;"
        cursor.execute(sql, (purchase_id,))
        res = cursor.fetchone()
        # print(result[5]) # time ==>  2025-05-24 15:00:22.143595 ==> to get just the year 2025
        yearOfPurchase = int((str(res[5]))[:4])
        monthOfPurchase = int((str(res[5]))[5:7]) #  ==> to get just the month
        if yearOfPurchase == thisYear:
            monthsOfThisYear[monthOfPurchase-1] += int(row[4])

        elif yearOfPurchase == lastYear:
            monthsOfLastYear[monthOfPurchase-1] += int(row[4])

    # Standard Deviation
    sum_x = sum(monthsOfLastYear)
    mean = sum_x/12
    variance = sum((x - mean) ** 2 for x in monthsOfLastYear) / (12 - 1)
    std_dev = variance ** 0.5

    # Average Sales
    media = (sum_x/12)
    # Recommended Monthly Stock
    recommended = round(media + std_dev)

    disconnection(conn,cursor)


    return render_template("adminViewStatistic.html", labels=labels, last_year=monthsOfLastYear, this_year=monthsOfThisYear,
                           std_dev=round(std_dev), media=round(media), recommended=recommended)


