### Explanation
**Alarm and Alarm Types**:

- Alarm is a base class that handles common alarm functionality, such as setting the alarm time, snoozing, and checking if the alarm should ring.
- SoundAlarm and VibrationAlarm inherit from Alarm and override the alert method to provide specific behavior for each alarm type.

**AlarmClock**:

- AlarmClock manages multiple alarms. It has methods to add alarms, check if they should ring, and display the current time.

**AlarmManager:**

- AlarmManager provides a higher-level interface for managing alarms, including creating, reading, updating, and deleting alarms.
- It uses an instance of AlarmClock to perform these operations.
