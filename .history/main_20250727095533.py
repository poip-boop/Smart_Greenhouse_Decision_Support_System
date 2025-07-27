# Importing libraries
import random
# To improve output readability by use of dataframes
import pandas as pd

# Smart Greenhouse Decision Support System (SGDSS)
# Simulates rule-based AI decisions over 10 hourly intervals

# Configuration 
intervals = 10
critical_alert_threshhold = 2  
moisture_history_window = 3  

# State trackers 
consecutive_alerts = 0
moisture_history = []

# Sensor simulation 
def get_sensor_data():
    """
    Simulate hourly sensor readings using the random module.
    """
    return {
        'temperature': round(random.uniform(20, 45), 1),
        'humidity': round(random.uniform(15, 80), 1),
        'light': random.randint(100, 1200),
        'soil_moisture': round(random.uniform(20, 80), 1),
        'co2': random.randint(300, 1500)
    }

# Control logic
# Watering control
def control_watering(soil_moisture, temperature, humidity):
    """
    Fuzzy logic for watering control.
    Returns: 'Skip Watering', 'Initiate Light Watering', or 'Initiate Watering'.
    """
    if soil_moisture < 35 and (humidity < 40 or temperature > 30):
        return 'Initiate Watering'
    if 35 <= soil_moisture <= 50 and temperature > 35:
        return 'Initiate Light Watering'
    if soil_moisture > 70:
        return 'Skip Watering'
    return 'Skip Watering'

# Shading control
def control_shading(light):
    """
    Switch-case style shading control based on light intensity.
    Returns: shading action string.
    """
    if light < 300:
        return 'Open Shades'
    elif light < 800:
        return 'No Action'
    elif light < 1000:
        return 'Close Partially'
    else:
        return 'Close Fully'

# AI driven risk alerts
def generate_alerts(data):
    """
    Rule-based alerts if 3 or more risk conditions met.
    Returns: (alert_flag: bool, active_conditions: list)
    """
    conditions = []
    if data['temperature'] > 36:
        conditions.append('High Temp')
    if data['humidity'] < 25:
        conditions.append('Low Humidity')
    if data['co2'] > 1200:
        conditions.append('High CO2')
    if data['soil_moisture'] < 30:
        conditions.append('Dry Soil')
    if data['light'] > 1100:
        conditions.append('Excess Light')

    alert_flag = len(conditions) >= 3
    return alert_flag, conditions

# Future watering trends
def recommend_future_watering(moisture_history):
    """
    Recommend next watering interval based on moving average of soil moisture.
    """
    if len(moisture_history) < moisture_history_window:
        return 'Insufficient data for recommendation'
    avg_moisture = sum(moisture_history[-moisture_history_window:]) / moisture_history_window
    if avg_moisture < 40:
        return 'Recommend watering in next interval'
    return 'Delay watering: moisture trending stable'


# Simulation Loop 
records = []

for hour in range(1, intervals + 1):
    data = get_sensor_data()
    watering_action = control_watering(data['soil_moisture'], data['temperature'], data['humidity'])
    shading_action  = control_shading(data['light'])
    alert_flag, conditions = generate_alerts(data)
    if alert_flag:
        consecutive_alerts += 1
    else:
        consecutive_alerts = 0
    critical_flag = consecutive_alerts > critical_alert_threshhold
    moisture_history.append(data['soil_moisture'])
    recommendation = recommend_future_watering(moisture_history)

    # collect
    records.append({
        'Hour': hour,
        'Temp(°C)': data['temperature'],
        'Hum(%)': data['humidity'],
        'Light(lux)': data['light'],
        'Soil(%)': data['soil_moisture'],
        'CO2(ppm)': data['co2'],
        'Watering': watering_action,
        'Shading': shading_action,
        'Alert': alert_flag,
        'Conditions': "; ".join(conditions),
        'Critical': critical_flag,
        'Recomm.': recommendation
    })

# Display neat output 
df = pd.DataFrame(records)
print(df.to_string(index=False))

# Test for critical flag 
def test_critical_flag():
    global consecutive_alerts
    consecutive_alerts = 0

    # Reading that triggers all 5 risk conditions
    alert_reading = {
        'temperature': 40.0,  
        'humidity': 10.0,     
        'co2': 1300,           
        'soil_moisture': 20.0, 
        'light': 1200         
    }

    # Simulate 3 iterations to check critical flag
    for i in range(1, 4):
        alert_flag, _ = generate_alerts(alert_reading)
        if alert_flag:
            consecutive_alerts += 1
        else:
            consecutive_alerts = 0

        critical_flag = consecutive_alerts > critical_alert_threshhold
        print(f"Iteration {i}: consecutive_alerts={consecutive_alerts}, critical_flag={critical_flag}")

    # At i==3, critical_flag should be True
    assert critical_flag is True, "Critical flag never raised!"

# run the test
test_critical_flag()
