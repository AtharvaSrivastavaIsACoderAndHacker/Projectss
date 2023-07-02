from os import system
system("cls")
import multiprocessing
import requests
from concurrent.futures import ProcessPoolExecutor
from datetime import date, timedelta


def download(urll, filename):
    print(f"Started Downloading {filename}")
    image_url = urll
    r = requests.get(image_url)
    file = filename + ".jpg"
    with open(file, 'wb') as f:
        f.write(r.content)
    print(f"Finished Downloading {filename}")

def urlFormat ():
      start_dt = date(2023, 2, 1)
      end_dt = date(2023, 7, 1)
      delta = timedelta(days=1)
      dates = []
      while start_dt <= end_dt:
            # add current date to list by converting  it to iso format
            dates.append(start_dt.isoformat())
            # increment start date by timedelta
            start_dt += delta
            urls = []
      i = 0
      for _ in dates:
            month = dates[i].split('-')[1]
            
            day = dates[i].split('-')[2]
            urls.append(f"https://epaperimg1.amarujala.com/2023/{month}/{day}/dl/01/hdimage.jpg")         
            i +=1
      # print(urls)
      return urls

def nam ():
      urls = urlFormat()
      k = 0
      names = []
      for _ in urls:
            name = str(urls[k].split('/')[4])+":"+str(urls[k].split('/')[5])
            names.append(name)
            k +=1
      # print(names)
      return names
      
            
      
            
            
if __name__ == '__main__': # -----------------------------------------------> this is import to run multiprocessing in windows
      
      
      processes = []
      
      urls = urlFormat()
      names = nam()

      for i, url in enumerate(urls):
            p = multiprocessing.Process(target=download, args=(url, str(i)))
            p.start()
            processes.append(p)

      for p in processes:
            p.join()