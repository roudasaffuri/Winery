from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd

# טעינת הנתונים
data = pd.read_csv('sales_data_with_prices.csv')

# המרת נתונים קטגוריאליים למספריים
data['Wine Type'] = data['Wine Type'].astype('category').cat.codes
data['Price Category'] = data['Price Category'].astype('category').cat.codes
data['Season'] = data['Season'].astype('category').cat.codes

# בחירת תכונות לניתוח
features = data[['Wine Type', 'Price Category', 'Season', 'Price']]

# יצירת מודל K-Means
kmeans = KMeans(n_clusters=4, random_state=0)
data['Cluster'] = kmeans.fit_predict(features)

# הצגת פיזור הנתונים
plt.scatter(data['Season'], data['Wine Type'], c=data['Cluster'], cmap='viridis')
plt.colorbar(label='Cluster')
plt.xlabel('Season')
plt.ylabel('Wine Type')
plt.title('Wine Clustering by Season')
plt.show()
