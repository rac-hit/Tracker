from datetime import datetime

def time_now():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    with open('time.txt', 'a', encoding='utf-8') as file:
        file.write('\n' + current_time)



