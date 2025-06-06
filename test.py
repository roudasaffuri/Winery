# from db_connection import create_connection
#
# def seasonalSt():
#     # Connect to PostgreSQL
#     conn = create_connection()
#     cursor = conn.cursor()
#
#     query = """ SELECT * FROM purchases; """
#
#     cursor.execute(query)
#     results = cursor.fetchall()
#
#
#     Autumn = []
#     Winter = []
#     Summer = []
#     Spring = []
#
#     def add_to_season(season_list, purchase_id):
#         query = """SELECT * FROM purchase_items WHERE purchase_id = %s;"""
#         cursor.execute(query, (purchase_id,))
#         purchases = cursor.fetchall()
#         for p in purchases:
#            # p[4] = wine name , p[4] = quantity
#             season_list.append((p[3], p[4]))
#
#     for row in results:
#         # Parse the month from the timestamp
#         # # row[5] = 2024-08-07 14:02:06.000636
#         month = int(str(row[5])[5:7])
#         purchase_id = row[0]
#
#
#         if month in [12, 1, 2]:
#             add_to_season(Winter, purchase_id)
#         elif month in [3, 4, 5]:
#             add_to_season(Spring, purchase_id)
#         elif month in [6, 7, 8]:
#             add_to_season(Summer, purchase_id)
#         elif month in [9, 10, 11]:
#             add_to_season(Autumn, purchase_id)
#
#
#     print("Autumn:", Autumn)
#     print("Summer:", Summer)
#     print("Spring:", Spring)
#     print("Winter:", Winter)
#
#     def sumTotalSeason(season):
#         totalWines=0
#         for s in season:
#             totalWines+=s[1]
#         return totalWines
#
#     totalAutumn = sumTotalSeason(Autumn)
#     totalWinter = sumTotalSeason(Winter)
#     totalSummer = sumTotalSeason(Summer)
#     totalSpring = sumTotalSeason(Spring)
#
#
#
#
#     print(f"totalSummer :{totalSummer}  , totalSpring:  {totalSpring}  ,totalAutumn:  {totalAutumn} ,  totalWinter:{totalWinter}")
#
#     AutumnItemPercent = []
#     WinterItemPercent  = []
#     SummerItemPercent  = []
#     SpringItemPercent  = []
#
#     for i in range(0,40) :
#
#         AutumnItemPercent.append((Autumn[i][0],(Autumn[i][1]/totalAutumn)*100))
#         WinterItemPercent.append((Winter[i][0],(Winter[i][1]/totalWinter)*100))
#         SummerItemPercent.append((Summer[i][0], (Summer[i][1] / totalSummer)*100))
#         SpringItemPercent.append((Spring[i][0], (Spring[i][1] / totalSpring)*100))
#
#     print(f" Autumn : {AutumnItemPercent}")
#     print(f"Winter : {WinterItemPercent}")
#     print(f"Summer :  {SummerItemPercent}")
#     print(f"Spring :  {SpringItemPercent}")
#     # Close the database connection
#     conn.close()
#
#     return {
#         "autumn": AutumnItemPercent,
#         "winter": WinterItemPercent,
#         "summer": SummerItemPercent,
#         "spring": SpringItemPercent
#     }
#
#
#
# # print(seasonalSt())