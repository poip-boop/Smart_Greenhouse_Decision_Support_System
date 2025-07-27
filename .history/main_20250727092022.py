import random

# Smart Greenhouse Decision Support System (SGDSS)
# Simulates rule-based AI decisions over 10 hourly intervals

#  Configuration 
intervals = 10
critical_alert_threshhold = 2  
moisture_history_window = 3  

# State Trackers 
consecutive_alerts = 0
moisture_history = []

# Sensor Simulation 
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

#  Control Logic
def control_watering(soil_moisture, temperature, humidity):
    """
    Fuzzy logic for watering control.
    Returns: 'No Water', 'Light Watering', or 'Full Watering'.
    """
    if soil_moisture < 35 and (humidity < 40 or temperature > 30):
        return 'Full Watering'
    if 35 <= soil_moisture <= 50 and temperature > 35:
        return 'Light Watering'
    if soil_moisture > 70:
        return 'No Water'
    return 'No Water'


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


def recommend_future_watering(moisture_history):
    """
    Bonus: Recommend next watering interval based on moving average.
    """
    if len(moisture_history) < MOISTURE_HISTORY_WINDOW:
        return 'Insufficient data for recommendation'
    avg_moisture = sum(moisture_history[-MOISTURE_HISTORY_WINDOW:]) / MOISTURE_HISTORY_WINDOW
    if avg_moisture < 40:
        return 'Recommend watering in next interval'
    return 'Delay watering; moisture trending stable'

# --- Simulation Loop ---
print(f"{'Hour':<5} {'Temp(°C)':<8} {'Hum(%)':<7} {'Light(lux)':<11} {'Soil(%)':<8} {'CO2(ppm)':<9} {'Watering':<15} {'Shading':<15} {'Alert':<6} {'Conditions':<40} {'CriticalFlag':<12} {'Recommendation'}")
for hour in range(1, INTERVALS + 1):
    data = get_sensor_data()
    # Control decisions
    watering_action = control_watering(data['soil_moisture'], data['temperature'], data['humidity'])
    shading_action = control_shading(data['light'])
    alert_flag, conditions = generate_alerts(data)

    # Track consecutive alerts for critical flag
    global consecutive_alerts
    if alert_flag:
        consecutive_alerts += 1
    else:
        consecutive_alerts = 0
    critical_flag = consecutive_alerts > CRITICAL_ALERT_THRESHOLD

    # Update moisture history for bonus
    moisture_history.append(data['soil_moisture'])
    recommendation = recommend_future_watering(moisture_history)

    # Display decisions
    print(f"{hour:<5} {data['temperature']:<8} {data['humidity']:<7} {data['light']:<11} {data['soil_moisture']:<8} {data['co2']:<9} {watering_action:<15} {shading_action:<15} {str(alert_flag):<6} {', '.join(conditions):<40} {str(critical_flag):<12} {recommendation}")
