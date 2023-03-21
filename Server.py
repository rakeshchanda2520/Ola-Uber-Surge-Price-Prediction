from flask import Flask, render_template, request
import travelling_time
from selenium import webdriver
import datetime
import pytz
import re

app = Flask(__name__)

# load the model
import pickle

file = open("price_rf.pk", 'rb')
model = pickle.load(file)
file.close()


@app.route("/", methods=["GET"])
def root():
    return render_template("index.html")


@app.route("/predict", methods=["GET"])
def predict():
    source = request.args.get('source')
    destination = request.args.get('destination')
    distance=2.5
    avg_travel_time=12
    driver = webdriver.Chrome(r"chromedriver_win32.exe")
    driver.minimize_window()
    source_1 = source + "+Boston,+MA,+USA"
    destination_1 = destination + "+Boston,+MA,+USA"
    travel_time = travelling_time.Time_travel(destination_1,
                                              source_1, driver)
    travel_time.car_button_click()

    ct = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))


    ts = ct.timestamp()

    y = travel_time.add_time_traveling(ts * 1000)

    y_1 = list(map(int, re.findall('\d+', y[0])))
    y_2 = re.findall("\d+\.\d+", y[1])

    print(y_1)
    print(y_2)
    if len(y_1) == 1:
        avg_travel_time = int(y_1[0])
    elif len(y_1) == 2:
        avg_travel_time = (int(y_1[0]) + int(y_1[1]))/2

    if len(y_2) == 1:
        distance = float(y_2[0])*1.60934
    print(y_2)
    print(source)
    print(destination)

    temp=40.130000
    clouds=0.780000
    pressure=1007.660000
    rain=0.014850
    humidity=0.760000
    wind=6.570000



    cab = str(request.args.get('cab_type'))
    if cab=='Uber':
        cab_type_Lyft=0
        cab_type_Uber=1
    else:
        cab_type_Lyft = 1
        cab_type_Uber = 0


    type = str(request.args.get('type'))
    name_Black=name_BlackSUV = name_Lux = name_LuxBlack = name_LuxBlackXL = name_Lyft = name_LyftXL = name_Shared = name_UberPool = name_UberX = name_UberXL = name_WAV = 0

    if type=='Uber -> Black':
        name_Black=1
    elif type=='Uber -> Black SUV':
        name_BlackSUV = 1
    elif type=='Uber -> Uber Pool':
        name_UberPool = 1
    elif type=='Uber -> Uber X':
        name_UberX=1
    elif type == "Uber -> WAV":
        name_WAV = 1
    elif type == "Lyft -> Shared":
        name_Shared = 1
    elif type == "Lyft -> Lux":
        name_Lux = 1
    elif type == "Lyft -> Lux Black":
        name_LuxBlack = 1
    elif type == "Lyft -> Lux Black XL":
        name_LuxBlackXL = 1
    elif type == "Lyft -> Lyft":
        name_Lyft = 1
    elif type == "Lyft -> Lyft XL":
        name_LyftXL = 1

    # surge_multiplier_1_0= surge_multiplier_1_25 = surge_multiplier_1_5= surge_multiplier_1_75 = surge_multiplier_2_0 = surge_multiplier_2_5 = surge_multiplier_3_0 = 0
    # surge_multiplier_1_0 = 1
    a=1
    b,c,d,e,f,g=0,0,0,0,0,0

    day = str(request.args.get('day'))
    day_0, day_1, day_2, day_3, day_4, day_5, day_6=0,0,0,0,0,0,0
    if day=='Sunday':
        day_0=1
    elif day=='Monday':
        day_1=1
    elif day=='Tuesday':
        day_2=1
    elif day=='Wednesday':
        day_3=1
    elif day=='Thursday':
        day_3=1
    elif day=='Friday':
        day_4=1
    elif day=='Saturday':
        day_5=1

    class_hour_0=class_hour_1=class_hour_2=class_hour_3=class_hour_4=class_hour_5=class_hour_6=class_hour_7=0

    class_hour_1=1

    print(day)
    print(type)
    print(avg_travel_time)
    print(distance)
    print(cab_type_Lyft)
    print(cab_type_Uber)
    predictions = model.predict([[distance,avg_travel_time,temp,clouds,pressure,rain,humidity,wind,cab_type_Lyft,cab_type_Uber,name_Black,name_BlackSUV,name_Lux,name_LuxBlack,name_LuxBlackXL,name_Lyft,name_LyftXL,name_Shared,name_UberPool,name_UberX,name_UberXL,name_WAV,a,b,c,d,e,f,g,day_0, day_1, day_2, day_3, day_4, day_5, day_6,class_hour_0,class_hour_1,class_hour_2,class_hour_3,class_hour_4,class_hour_5,class_hour_6,class_hour_7]])
    result = f"Your Fare Price Should be Around =  ${predictions[0]}"
    return render_template("result.html", html_result=result)


app.run(port=8080, debug=True, host="0.0.0.0")
