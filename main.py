import mysql.connector
import random
mydb = mysql.connector.connect(
host="localhost",
user="root",
password="",
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
def stat_formatter(stats):
    print("Games played:",stats[4])
    print("Wins:",stats[5])
    print("Losses",stats[6])
    print("Win percentage:",stats[7],'%')
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
    with open('words.txt','r') as t:
        a=t.readlines()
        a=[i.strip() for i in a]
        word_full=random.choice(a)
    word=word_full.lower()
    progress=[]
    for letter in word:
        if letter!=" ":
            progress.append("?")
        else:
            progress.append(" ")

    print(progress)
    game_status=0
    while guesses<6:
        guess=input("Enter letter")
        guess=guess.lower()
        if len(guess)>1:
            print("Too many letters")
            continue
        if guess in word and guess not in letters_used:
            print("correct")
            letters_used.append(guess)
            hangman_graphic(guesses)
            progress=progress_updater(guess,word,progress,word_full)
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
            progress=progress_updater(guess,word,progress,word_full)
            print("progress:"+"".join(progress))
            print("Letters used:"+",".join(letters_used))
        else:
            print("Letter already used")
            print("try again")
    return [game_status,word_full]

def progress_updater(guess,word,progress,word_full):
    i=0
    while i<len(word):
        if guess==word[i]:
            progress[i]=word_full[i]
            i+=1
        else:
            i+=1
    return progress

global stats
def game_execute():   
    while True:
        print("Welcome to Hangman:")
        ch=int(input("Would you like to sign up(1) or login(2) for saving stats or play as a guest(3) or exit(4)?"))
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
            pwd=input("Enter your password")
            s=login(user_id,pwd)
            if len(s)==0:
                print("Invalid username or password Please try again.If you do not have an account Please make one before attempting to log in")
                continue
            else:
                stats=list(login(user_id,pwd)[0])
            break
        elif ch==3:
            #issue
            print("Warning! Your stats wont be saved")
            c=int(input("Would you like to go back(1) or continue(2)"))
            print(c)
            if c==1:
                print("going back")
                continue
            elif c==2:
                print("continuing")
                stats=['#', 'Guest', 'guest', 'guest', 0, 0, 0, 0.0 ]
                break
            else:
                print("Invalid input")
                continue
        
        elif ch==4:
            print("Exitting now")
            exit()
        else:
            print("try again")
            continue
    while True:
        ch2=int(input("Would you like to play(1) or see stats(2) or exit(3) or go to home screen(4)"))
        if ch2==1:
            game_status=core_game()
            if game_status[0]==0:
                print("You LOSE!")
                print("Word was:"+game_status[1])
            stats=update(game_status,stats)
            update_db(stats) 
            stat_formatter(stats)
            continue
        elif ch2==2:
            stat_formatter(stats)

            continue
        elif ch2==3:
            break
        elif ch2==4:
            game_execute()
        else:
            print("Invalid input")
            continue
game_execute()



