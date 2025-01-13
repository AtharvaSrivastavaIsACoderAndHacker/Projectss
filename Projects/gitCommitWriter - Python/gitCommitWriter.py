import datetime
import pyperclip
datetimee = datetime.datetime.now()
string = f"{datetimee.day}/{datetimee.month}/{datetimee.year} {datetimee.hour:02}:{datetimee.minute:02} ++_()"
pyperclip.copy(string)