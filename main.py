import mysql.connector
mydb = mysql.connector.connect(
host="localhost",
user="root",
password="#alex2005",
database="HANGMAN_PROJECT"
)
def register(Name,User_id,Password):
        mycursor = mydb.cursor()
        query="insert into main_table(Name,User_id,Password) values(%s,%s,%s);"
        t=(Name,User_id,Password)
        a=0
        try:
            mycursor.execute(query,t)
            mydb.commit()
            print("Signup successful")
        except:
            print("Invalid userid or password please try again")
            a=1
            return a

def login(User_id,Password):
        mycursor=mydb.cursor()
        query="Select * from main_table where User_id=%s and Password=%s"
        t=(User_id,Password)
        mycursor.execute(query,t)
        stats=mycursor.fetchall()
        return stats

def hangman_graphic(guesses):   
        if guesses == 0:
            print("________      ")
            print("|      |      ")
            print("|             ")
            print("|             ")
            print("|             ")
            print("|             ")
        elif guesses == 1:
            print("________      ")
            print("|      |      ")
            print("|      0      ")
            print("|             ")
            print("|             ")
            print("|             ")
        elif guesses == 2:
            print("________      ")
            print("|      |      ")
            print("|      0      ")
            print("|     /       ")
            print("|             ")
            print("|             ")
        elif guesses == 3:
            print("________      ")
            print("|      |      ")
            print("|      0      ")
            print("|     /|      ")
            print("|             ")
            print("|             ")
        elif guesses == 4:
            print("________      ")
            print("|      |      ")
            print("|      0      ")
            print("|     /|\     ")
            print("|             ")
            print("|             ")
        elif guesses == 5:
            print("________      ")
            print("|      |      ")
            print("|      0      ")
            print("|     /|\     ")
            print("|     /       ")
            print("|             ")
        else:
            print("________      ")
            print("|      |      ")
            print("|      0      ")
            print("|     /|\     ")
            print("|     / \     ")
            print("|             ")
            print("GAME OVER!")

def update(game_status,stats):
    if game_status==0:
        stats[4]+=1
        stats[6]+=1
        stats[7]=(stats[5]/stats[4])*100
        return stats
    elif game_status==1:
        stats[4]+=1
        stats[5]+=1
        stats[7]=(stats[5]/stats[4])*100
    return stats
def update_db(stats):
    if stats[0]!='#':
        mycursor=mydb.cursor()
        query="replace into main_table values(%s,%s,%s,%s,%s,%s,%s,%s);"
        t=tuple(stats)
        mycursor.execute(query,t)
        mydb.commit()
        print("DB updated")

def core_game():
    guesses=0
    letters_used=[]
    word="test"
    progress = ["?"]*len(word)
    game_status=0
    while guesses<6:
        guess=input("Enter letter")
        if len(guess)>1:
            print("Too many letters")
            continue
        if guess in word and guess not in letters_used:
            print("correct")
            letters_used.append(guess)
            hangman_graphic(guesses)
            progress=progress_updater(guess,word,progress)
            print("progress:"+"".join(progress))
            print("Letters used:"+",".join(letters_used))
            if "?" not in progress:
                print("You Win")
                game_status=1
                break
        elif guess not in word and guess not in letters_used:
            guesses+=1
            print("Wrong")
            letters_used.append(guess)
            hangman_graphic(guesses)
            progress=progress_updater(guess,word,progress)
            print("progress:"+"".join(progress))
            print("Letters used:"+",".join(letters_used))
        else:
            print("Letter already used")
            print("try again")
    return game_status

def progress_updater(guess,word,progress):
    i=0
    while i<len(word):
        if guess==word[i]:
            progress[i]=guess
            i+=1
        else:
            i+=1
    return progress

while True:
    print("Welcome to Hangman:")
    ch=int(input("Would you like to sign up(!) or login(2) for saving stats or play as a guest(3)?"))
    if ch==1:
        name=input("Enter your name:")
        user_id=input("Enter username:")
        pwd=input("Enter password:")
        a=register(name,user_id,pwd)
        if a==0:
            print("please sign in now")
            continue
        elif a==1:
            continue
    elif ch==2:
        user_id=input("Enter your userid")
        pwd=input("Enter your pwd")
        s=login(user_id,pwd)
        if len(s)==0:
            print("Invalid username or password Please try again.If you do not have an account Please make one before attempting to log in")
            continue
        else:
            stats=list(login(user_id,pwd)[0])
            print(stats)
        break
    elif ch==3:
        print("Warning your stats wont be saved")
        ch2=print("Would you like to make an account or login")
        if ch2==1:
            continue
        else:
            stats=['#', 'Guest', 'guest', 'guest', 0, 0, 0, 0.0 ]
            break
    else:
        print("try again")
        continue
while True:
    ch2=int(input("Would you like to play or see stats or exit"))
    if ch2==1:
        game_status=core_game()
        print(game_status)
        print(stats)
        stats=update(game_status,stats)
        print("Your new stats are:",stats)
        update_db(stats)
        
        continue
    elif ch2==2:
        print(stats)
        continue
    elif ch2==3:
        break
    else:
        print("Invalid input")
        continue




