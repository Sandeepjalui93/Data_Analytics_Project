import pandas as pd
import mysql.connector as connection
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")

HOST = 'localhost'
USERNAME = 'root'
PASSWORD = ''
DATABASE = 'myntra'

def connecting_db_and_loading_data():
    query = "select * from cleandata;"
    mydb = connection.connect(host=HOST, port="3306", database=DATABASE, user=USERNAME, passwd=PASSWORD)
    df = pd.read_sql(query, mydb)
    return df

def top_ratings():
    data = connecting_db_and_loading_data()
    return len(data[data["avg_rating"]>4]["ratingCount"]>2000)

print("There are",top_ratings(),"ratings for avg_rating above 4 and ratingcount above 2000")

data = connecting_db_and_loading_data()
new_data = data[(data['avg_rating']>4.4)&(data['ratingCount']>3000)]
print('The top 10 products with avg_rating above 4.4 and ratingcount above 3000 are',new_data.head(10))

#Average rating plot
gk=connecting_db_and_loading_data().groupby(["brand"]).agg({"avg_rating":["mean"]})
xaxis=gk.index.values
yaxis=gk.reset_index()['avg_rating']['mean']
plt.plot(xaxis,yaxis)
plt.show()