import os
folder = os.listdir('clutter')
print(folder)
i = 0
for f in folder:
      os.rename(f"clutter/{folder[i]}", f"clutter/{i}")
      print(folder[i])
      i+=1