from db_connection import create_connection

# Connect to PostgreSQL
conn = create_connection()

# SQL query to get total quantity of each wine per season
query = """
SELECT
    CASE
        WHEN EXTRACT(MONTH FROM p.purchased_at) IN (12, 1, 2) THEN 'Winter'
        WHEN EXTRACT(MONTH FROM p.purchased_at) IN (3, 4, 5) THEN 'Spring'
        WHEN EXTRACT(MONTH FROM p.purchased_at) IN (6, 7, 8) THEN 'Summer'
        WHEN EXTRACT(MONTH FROM p.purchased_at) IN (9, 10, 11) THEN 'Autumn'
    END AS season,
    pi.wine_name,
    SUM(pi.quantity) AS total_quantity_sold
FROM purchase_items pi
JOIN purchases p ON pi.purchase_id = p.purchase_id
GROUP BY season, pi.wine_name
ORDER BY season, pi.wine_name;
"""

# Execute SQL query and fetch results
cursor = conn.cursor()
cursor.execute(query)
results = cursor.fetchall()

# Close the database connection
conn.close()

# Initialize empty lists for each season
Autumn = []
Winter = []
Summer = []
Spring = []

# Process the results and append to appropriate season list
for row in results:
    season = row[0]
    wine_name = row[1]
    total_quantity_sold = row[2]

    if season == 'Autumn':
        Autumn.append((wine_name, total_quantity_sold))
    elif season == 'Winter':
        Winter.append((wine_name, total_quantity_sold))
    elif season == 'Summer':
        Summer.append((wine_name, total_quantity_sold))
    elif season == 'Spring':
        Spring.append((wine_name, total_quantity_sold))

# Print the results
print("Autumn:", Autumn)
print("Summer:", Summer)
print("Spring:", Spring)
print("Winter:", Winter)


totalAutumn = 0
totalWinter = 0
totalSummer = 0
totalSpring = 0

for i in range(0,40) :
    totalAutumn += Autumn[i][1]
    totalSpring += Spring[i][1]
    totalSummer += Summer[i][1]
    totalWinter += Winter[i][1]
print(f"totalSummer :{totalSummer}  , totalSpring:  {totalSpring}  ,totalAutumn:  {totalAutumn} ,  totalWinter:{totalWinter}")

AutumnItemPercent = []
WinterItemPercent  = []
SummerItemPercent  = []
SpringItemPercent  = []

for i in range(0,40) :

    AutumnItemPercent.append((Autumn[i][0],(Autumn[i][1]/totalAutumn)))
    WinterItemPercent.append((Winter[i][0],(Winter[i][1]/totalWinter)))
    SummerItemPercent.append((Summer[i][0], (Summer[i][1] / totalSummer)))
    SpringItemPercent.append((Spring[i][0], (Spring[i][1] / totalSpring)))

print(AutumnItemPercent)
print(WinterItemPercent)
print(SummerItemPercent)
print(SpringItemPercent)





