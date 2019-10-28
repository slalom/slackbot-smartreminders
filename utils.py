from datetime import datetime, date, timedelta
import dateutil
import sys
import calendar
import math
from dateutil.rrule import rrule, MONTHLY

def find_start_date(month, year, numWeek, weekday, startHour, startMinute):
  cal = calendar.monthcalendar(year, month)
  
  if(cal[0][weekday] == 0):
    numWeek += 1
  
  startDate = cal[numWeek][weekday]

  return datetime(year, month, startDate, startHour, startMinute)

def list_all_dates(month, year, numWeek, weekday, startHour, startMinute):
  startDate = find_start_date(month, year, numWeek, weekday, startHour, startMinute)

  # if the start of the recurrance occurs before today's date, start at the next month
  if(startDate < datetime.now()):
    if(startDate.month == 12):
      startDate = find_start_date(1, year, numWeek, weekday, startHour, startMinute)
    else:
      startDate = find_start_date(month + 1, year, numWeek, weekday, startHour, startMinute)

  # scheduled messages can only be scheduled out 120 days
  endDate = startDate + timedelta(days=120)

  monthlist = ((startDate.month, startDate.year) for startDate in rrule(MONTHLY, dtstart=startDate, until=endDate))

  dates = []
  for months in monthlist:
    dates.append(find_start_date(months[0], months[1], numWeek, weekday, startHour, startMinute).strftime("%s"))

  return dates

def parse_command(command):
  possible_occurance = {
    "first": 0,
    "second": 1,
    "third": 2,
    "fourth": 3
  }
  possible_days = {
    'Monday': 0, 
    'Tuesday': 1, 
    'Wednesday': 2, 
    'Thursday': 3, 
    'Friday': 4, 
    'Saturday': 5, 
    'Sunday': 6
  }

  # split the messages from the recurrence
  command = command.split(' every ')
  reminder_body = command[0]
  recurrence = command[1].split(' ')

  if(recurrence[0] not in possible_occurance.keys()):
    return recurrence[0] + " is not a valid start occurance"

  if(recurrence[1] not in possible_days.keys()):
    return recurrence[1] + " is not a valid start date"

  currentYear = datetime.now().year
  currentMonth = datetime.now().month

  startWeek = possible_occurance[recurrence[0]]
  startWeekDay = possible_days[recurrence[1]]

  time = recurrence[3]
  mode = time[-2:]
  
  if(len(time) == 6):
    startHour = int(time[0])
    startMinute = int(time[2:4])
  else:
    startHour = int(time[:-5])
    startMinute = int(time[3:5])
  
  if startHour < 12 and mode == 'pm':
    startHour += 12
  if startHour == 12 and mode == 'am':
    startHour = 0

  dates = list_all_dates(currentMonth, currentYear, startWeek, startWeekDay, startHour, startMinute)

  return {
    'text': reminder_body,
    'scheduled_dates': dates
  }
  
 

if __name__ == "__main__":
  command = "make a cup of coffee every fourth Thursday at 5:30am"
  print(parse_command(command))