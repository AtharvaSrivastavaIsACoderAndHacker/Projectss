from os import system

class Libraryy:
      
      with open("books.txt", "r") as f:
            books = f.readlines()     
                              
      with open("studentsBorrowed.txt", "r") as f:
            students = f.readlines()
            
      NoOfTotalBooks = len(books)
      CurrentAvailableBooks = NoOfTotalBooks - len(students)
      
      
      
      def borrow(nameOfStudent,BookName):
            with open("books.txt", "r") as f:
                  books = f.readlines()    
            with open("studentsBorrowed.txt", "r") as f:
                  students = f.readlines()
                  
                        
            query = BookName+"\n"    
            if query in books:   
                  li = ""                
                  for lines in students:
                        li = str(lines) 
                        
                  if BookName in li:
                        print("Sorry ! Your Desired Book Is Already Borrowed !")                  
                  else:
                        with open("studentsBorrowed.txt", "a") as f:
                              f.write(f"{nameOfStudent} {BookName}\n")
            
                              print("Please Recieve Your Book !")         
            else:
                  print("Your Desired Book Is'nt Available In Our Library !")                  
                  
                  
      def returnbook(nameOfStudent,BookName):
            with open("books.txt", "r") as f:
                  books = f.readlines()    
            with open("studentsBorrowed.txt", "r") as f:
                  students = f.readlines()
                  
                             
            query = BookName+"\n"
            if query in books:
                  li = ""               
                  for lines in students:
                        li = str(lines) 
                        
                  queryy = f"{nameOfStudent} {BookName}"
                  
                  if queryy in li:
                        with open("studentsBorrowed.txt", "w") as f:
                              for line in students:
                                    if queryy not in line:
                                          f.write(line)
                                  
                             
                              
                        print("Thanks For Returning The Book ! Hope you Enjoyed Reading ! :) ") 
                  else:
                        print("You Have'nt Borrowed This Book ! Our Record Says : "+queryy)                  
                                       
            else:
                  print("Jo Book Dene Aaye Ho Wo Iss Library Ki Hai Hi Nhi !") 
                
      
      
      
# ============================================================================================================================================

      
      
o = Libraryy
system("cls")
print('1. Borrow A Book')
print('2. Return A Book')
choice = int(input("Option :- "))

if(choice == 1 or choice == 2):
    print("")
else:
    raise ValueError("Only Integers 1 & 2 Are Valid !")

if(choice == 1):
    system("cls")
    name = input("Enter Your Name : ")
    book = input("Enter The Book's Name : ")
    o.borrow(name,book)
if(choice == 2):
    system("cls")
    name = input("Enter Your Name : ")
    book = input("Enter The Book's Name : ")
    o.returnbook(name,book)
    
     
      
         