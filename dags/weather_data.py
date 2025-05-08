import requests,time
from snowflake import connector
from datetime import datetime
import pytz 

# data=[{'City': 'Vellore,India', 'lattitude': '12.933', 'longitude': '79.133', 'temperature': 37, 'wind speed': 6, 'humidity': 27}, {'City': 'Chennai,India', 'lattitude': '13.083', 'longitude': '80.283', 'temperature': 35, 'wind speed': 32, 'humidity': 56}, {'City': 'Ulundurpettai,India', 'lattitude': '11.700', 'longitude': '79.283', 'temperature': 35, 'wind speed': 24, 'humidity': 41}, {'City': 'Delhi,India', 'lattitude': '28.667', 'longitude': '77.217', 'temperature': 35, 'wind speed': 20, 'humidity': 37}]

def creating_link_for_places(places,apikey):
    data_list=[]
    for place in places:
        final={}
        try:
            link=f'''http://api.weatherstack.com/current?access_key={apikey}&query={place}'''
            time.sleep(1)
            res=requests.get(link)
            data=res.json()
            final["City"]=f"{data['location']['name']},{data['location']['country']}" 
            final["lattitude"]=data['location']["lat"]
            final["longitude"]=data['location']["lon"]
            final["temperature"]=data['current']['temperature']
            final["wind speed"]=data['current']['wind_speed']
            final["humidity"]=data['current']['humidity']
            data_list.append(final)
        except Exception as e:
            print("you api key is expired..")
            continue
    return data_list

def inserting_into_snowflake(data):
    conn=connector.connect(
        user="Devanathan",
        password="devA21032000002",
        account="RNXMYMU-VG86367",
        warehouse="COMPUTE_WH",
        database="FIRST_DATABASE",
        schema="PUBLIC"
    )

    cursor=conn.cursor()

    try:
        cursor.execute('''create table weather_api(
                   id int autoincrement,
                   City string,
                   lattitude string,
                   longitude string,
                   temperature string,
                   wind_speed string,
                   humidity string,
                   date_time TIMESTAMP
                       )''')
    except Exception as e:
        print(e)
        pass
    insert_list=[]
    
    localtz=pytz.timezone('Asia/Kolkata')
    print(localtz)
    for value in data:
        final=list(value.values())
        final.append(datetime.now(localtz))
        insert_list.append(tuple(final)) 
    try:
        cursor.executemany('''insert into weather_api (
        city, lattitude, longitude, temperature, wind_speed, humidity, date_time
    ) values(%s,%s,%s,%s,%s,%s,%s)''',insert_list)
    except Exception as e:
        print(e)
        print("error while entering data")
    print(cursor.execute("SELECT CURRENT_VERSION()").fetchone())


if __name__=="__main__":
    key='6d5c765de6dadc62952354d0272b3b4b'
    places=["vellore",'chennai','ulundurpet','delhi,India']
    data=creating_link_for_places(places,key)
    inserting_into_snowflake(data)
    