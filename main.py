from datetime import datetime, timedelta
import time
import pytz

IST = pytz.timezone('Asia/Kolkata')
daynames = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thur', 4:'Fri', 5:'Sat', 6:'Sun'}

class Alarm:
    def __init__(self, alarm_time, day_of_week):
        if alarm_time.tzinfo is None:
            self.alarm_time = IST.localize(alarm_time)
        else:
            self.alarm_time = alarm_time
        self.day_of_week = day_of_week
        self.day_name = daynames[day_of_week]
        self.snoozed = False
        self.snooze_time = None
        self.snooze_count = 0
        self.max_snoozes = 3

    def __str__(self):
        return f"Alarm set for {self.day_name} at {self.alarm_time.strftime('%H:%M:%S')}"

    def set_snooze(self, snooze_minutes=5):
        if self.snooze_count < self.max_snoozes:
            self.snooze_time = datetime.now(IST) + timedelta(minutes=snooze_minutes)
            self.snoozed = True
            self.snooze_count += 1
            print(f"Alarm snoozed for {snooze_minutes} minutes. Snooze count: {self.snooze_count}")
        else:
            print("Maximum snoozes reached. Cannot snooze further.")

    def check_alarm(self, current_time):
        if self.snoozed and self.snooze_time:
            if current_time >= self.snooze_time:
                self.snoozed = False
                self.snooze_time = None
                return True
        elif current_time.weekday() == self.day_of_week and current_time.time() >= self.alarm_time.time():
            return True
        return False

    def alert(self):
        raise NotImplementedError("This method should be implemented by subclasses")

class SoundAlarm(Alarm):
    def alert(self):
        print("Sound alarm ringing!", self)

class VibrationAlarm(Alarm):
    def alert(self):
        print("Vibration alarm ringing!", self)

class AlarmClock:
    def __init__(self):
        self.alarms = []

    def display_current_time(self):
        now = datetime.now(IST)
        print("Current time:", now.strftime('%Y-%m-%d %H:%M:%S'))
        return now

    def add_alarm(self, alarm):
        self.alarms.append(alarm)
        print(f"Alarm added: {alarm}")

    def check_alarms(self):
        current_time = self.display_current_time()
        for alarm in self.alarms:
            if alarm.check_alarm(current_time):
                alarm.alert()
                snooze = input("Snooze? (y/n): ")
                if snooze.lower() == 'y':
                    alarm.set_snooze()
                else:
                    print("Alarm turned off.")
                    self.alarms.remove(alarm)
            else:
                remaining_time = alarm.alarm_time - current_time if not alarm.snoozed else alarm.snooze_time - current_time
                print(f"Time remaining for {alarm}: {remaining_time}")

    def start(self):
        try:
            while True:
                self.check_alarms()
                time.sleep(1)
        except KeyboardInterrupt:
            print("Alarm clock stopped.")

class AlarmManager:
    def __init__(self):
        self.alarm_clock = AlarmClock()

    def create_alarm(self, alarm_type, alarm_time, day_of_week):
        if alarm_type == 'sound':
            alarm = SoundAlarm(alarm_time, day_of_week)
        elif alarm_type == 'vibration':
            alarm = VibrationAlarm(alarm_time, day_of_week)
        else:
            raise ValueError("Invalid alarm type. Choose 'sound' or 'vibration'.")
        self.alarm_clock.add_alarm(alarm)

    def read_alarms(self):
        for idx, alarm in enumerate(self.alarm_clock.alarms, start=1):
            print(f"{idx}: {alarm}")

    def update_alarm(self, index, new_alarm_time=None, new_day_of_week=None):
        if 0 <= index < len(self.alarm_clock.alarms):
            alarm = self.alarm_clock.alarms[index]
            if new_alarm_time:
                if new_alarm_time.tzinfo is None:
                    new_alarm_time = IST.localize(new_alarm_time)
                alarm.alarm_time = new_alarm_time
            if new_day_of_week is not None:
                alarm.day_of_week = new_day_of_week
            print(f"Updated alarm {index + 1}: {alarm}")
        else:
            print("Invalid alarm index.")

    def delete_alarm(self, index):
        if 0 <= index < len(self.alarm_clock.alarms):
            removed_alarm = self.alarm_clock.alarms.pop(index)
            print(f"Deleted alarm {index + 1}: {removed_alarm}")
        else:
            print("Invalid alarm index.")

    def get_alarm_count(self):
        return len(self.alarm_clock.alarms)

    def start_alarm_clock(self):
        self.alarm_clock.start()

if __name__ == "__main__":
    manager = AlarmManager()

    current_time = datetime.now(IST)
    alarm_time_1 = current_time + timedelta(minutes=1)  # Set alarm for 1 minute from current time
    alarm_time_2 = current_time + timedelta(minutes=2)  # Set another alarm for 2 minutes from current time

    manager.create_alarm('sound', alarm_time_1, current_time.weekday())
    manager.create_alarm('vibration', alarm_time_2, current_time.weekday())

    manager.read_alarms()
    print(f"Number of alarms set: {manager.get_alarm_count()}")

    # manager.update_alarm(0, new_alarm_time=current_time + timedelta(minutes=3))
    manager.read_alarms()

    # manager.delete_alarm(1)
    # manager.read_alarms()
    print(f"Number of alarms set: {manager.get_alarm_count()}")

    manager.start_alarm_clock()



