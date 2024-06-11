import tkinter as tk
from PIL import Image, ImageTk
import random
import time
from odf import text, teletype
from odf.opendocument import load
import sys
import os
from playsound import playsound
import pygame

window=tk.Tk()
window.geometry("800x500")
window.resizable(False, False)
window.configure(bg='#b3e9d1')
window.title("HangMan")

image_path = "/home/asiman/Pictures/HANGMAN3.png"
bg = tk.PhotoImage(file=image_path)
label1 = tk.Label( window, image = bg) 
label1.place(x = 50, y=100)

pygame.mixer.init()
def music():
    pygame.mixer.music.load("/home/asiman/Downloads/button-124476.mp3")
    pygame.mixer.music.play()

def click_music():
    pygame.mixer.music.load("/home/asiman/Downloads/mouse-click-153941.mp3")
    pygame.mixer.music.play()

def win_music():
    pygame.mixer.music.load("/home/asiman/Downloads/success-fanfare-trumpets-6185.mp3")
    pygame.mixer.music.play()

def lose_music():
    pygame.mixer.music.load("/home/asiman/Downloads/mixkit-retro-arcade-lose-2027.wav")
    pygame.mixer.music.play()

def PlayGame():
    nickname = entry_nickname.get()
    if nickname == "":
        Label_ask = tk.Label(window,text="Please, enter nickname.", font=('Helvetica 20 italic'),fg = "#96151e", bg = "#b3e9d1")
        Label_ask.place(x=400,y=200)
        return    

    def win(nickname):       
        win_music()
        new_window.destroy()
        window=tk.Tk()
        window.geometry("400x300")
        window.resizable(False, False)
        window.configure(bg='#b3e9d1')
        window.title("Game Over")
        GameOver= tk.Label(text = "Game Over",font = 'Times 50  ',fg = "green",bg='#b3e9d1')
        GameOver.pack()
        Win= tk.Label(text = "Dear "+str(nickname),font = 'Times 30  ',fg = "black",bg='#b3e9d1')
        Win.pack()
        Win2= tk.Label(text = "You won!",font = 'Times 30  ',fg = "black",bg='#b3e9d1')
        Win2.pack()
        Again= tk.Label(text = "Do you want to play again? ",font = 'Times 25  bold',fg = "red",bg='#b3e9d1')
        Again.pack()
        Button_Yes = tk.Button(text = "Yes",font = 'Times 25  bold',fg = "red",bg='#b3e9d1',bd =5,command= lambda: [click_music(),RestartGame(window)])
        Button_Yes.place(x=90,y=210)
        Button_No = tk.Button(text = "No",font = 'Times 25  bold',fg = "red",bg='#b3e9d1', bd =5, command= lambda: [click_music(),Destroy()])
        Button_No.place(x=270,y=210)

    def lose(nickname):
        lose_music()
        new_window.destroy()
        window=tk.Tk()
        window.geometry("400x300")
        window.resizable(False, False)
        window.configure(bg='#b3e9d1')
        window.title("Game Over")
        GameOver= tk.Label(text = "Game Over",font = 'Times 50  ',fg = "green",bg='#b3e9d1')
        GameOver.pack()
        Win= tk.Label(text = "Dear "+str(nickname),font = 'Times 30  ',fg = "black",bg='#b3e9d1')
        Win.pack()
        Win2= tk.Label(text = "You lost!",font = 'Times 30  ',fg = "black",bg='#b3e9d1')
        Win2.pack()
        Again= tk.Label(text = "Do you want to play again? ",font = 'Times 25  bold',fg = "red",bg='#b3e9d1')
        Again.pack()
        Button_Yes = tk.Button(text = "Yes",font = 'Times 25  bold',fg = "red",bg='#b3e9d1',bd =5, command= lambda: [click_music(),RestartGame(window)])
        Button_Yes.place(x=90,y=210)
        Button_No = tk.Button(text = "No",font = 'Times 25  bold',fg = "red",bg='#b3e9d1', bd =5, command= lambda: [click_music(),Destroy()])
        Button_No.place(x=270,y=210)

    def RestartGame(window):
        window.destroy()
        def start_new_game():            
            script_path = '/home/asiman/Desktop/PythonProjects/hangman_game.py'        
            os.system(f'python3 {script_path}')
        start_new_game()      
    
    def Destroy():
        window.quit()    

    window.destroy()
    new_window =tk.Tk()
    new_window.configure(bg='#b3e9d1')
    new_window.title("Hang Man")

    new_window.geometry("800x500")
    new_window.resizable(False, False)

    file_path = '/home/asiman/Desktop/hangman_words.odt'
    doc = load(file_path)
    content = []
    for text_node in doc.getElementsByType(text.P):
        content.append(teletype.extractText(text_node))
    words = [line.strip() for line in content if line.strip()]
    selected_word = random.choice(words)
    print(selected_word)

    Label = tk.Label(new_window, text=len(selected_word)*" _" , font=('Helvetica 30 bold'),fg = "#257c65", bg='#b3e9d1')
    Label.place(x= 60,y=55)
    label_text = len(selected_word)*" _" 
    
    bgimg = Image.open("/home/asiman/Pictures/start.png")
    new_image = ImageTk.PhotoImage(bgimg)

    limg = tk.Label(new_window, image=new_image)
    limg.place(x=410,y=120)


    def Hint():
        nonlocal count_hint
        nonlocal selected_word
        count_hint -= 1
        
        def LetterSelect(selected_word):
            letters = []
            for i in selected_word:
                letters.append(i)
            letter = random.choice(letters)
            letter = letter.upper()
            return letter
        
        random_letter = LetterSelect(selected_word)
        nonlocal label_text
        while random_letter   in label_text:       
            random_letter = LetterSelect(selected_word)

        selected_word=selected_word.upper()
        indices = [i for i, letter in enumerate(selected_word) if letter == random_letter]
        for index in indices:
            label_index = 2*index+1
            label_text = label_text[:label_index] + random_letter + label_text[label_index + 1:]
         
        Label_text = tk.Label(new_window, text=label_text, font=('Helvetica 30 bold'),fg = "#257c65", bg='#b3e9d1')
        Label_text.place(x= 60,y=55)
        nonlocal hint_count_label

        if count_hint ==0:
            hint_count_label.destroy()
             
        else:
            hint_count_label.config(text=str(count_hint))

        if "_" not in label_text:
            Label_text = tk.Label(new_window, text=label_text, font=('Helvetica 30 bold'),fg = "#257c65", bg='#b3e9d1')
            Label_text.place(x= 60,y=55)
            new_window.after(1000, lambda nickname=nickname: win(nickname))
                                    

        if count_hint == 0:
            hint_button.destroy()                  

    bgimg = Image.open("/home/asiman/Downloads/rsz_hint2.png")
    hint_image = ImageTk.PhotoImage(bgimg)

    hint_button = tk.Button(new_window, image=hint_image, bd =4, command= lambda: [music(),Hint()])
    hint_button.place(x=705,y=30)

    count_hint =5
    hint_count_label = tk.Label(new_window, text = str(count_hint), font = "Times 35 italic bold",bg='#b3e9d1')
    hint_count_label.place(x= 673, y=50)

    attempt = tk.IntVar()
    attempt.set(0)

    def ClickLetter(text,selected_word):   
        selected_word = selected_word.upper()
        
        if text in selected_word:
            nonlocal label_text
            indices = [i for i, letter in enumerate(selected_word) if letter == text]
            for index in indices:
                index_game = index * 2 + 1
                m = label_text[index_game]
                n = selected_word[index]
                label_text = label_text[:index_game] + n + label_text[index_game + 1:]
               
            nonlocal Label
            Label.pack_forget()
            tk.Label(new_window, text=label_text, font=('Helvetica 30 bold'),fg = "#257c65", bg='#b3e9d1').place(x= 60,y=55)

            if "_" not in label_text:
                Label_text = tk.Label(new_window, text=label_text, font=('Helvetica 30 bold'),fg = "#257c65", bg='#b3e9d1')
                Label_text.place(x= 60,y=55)

                new_window.after(1000, lambda nickname=nickname: win(nickname))
                            
        else:
            nonlocal attempt 
            nonlocal limg
            attempt.set(attempt.get() + 1)
            if attempt.get() == 1:
                limg.pack_forget()
                bgimg = Image.open("/home/asiman/Pictures/1hangman.png")
                global new_image
                new_image = ImageTk.PhotoImage(bgimg)
                limg = tk.Label(new_window, image=new_image)
                limg.place(x=410,y=120)
            elif attempt.get() == 2:
                limg.pack_forget()
                bgimg = Image.open("/home/asiman/Pictures/2hangman.png")
                new_image = ImageTk.PhotoImage(bgimg)
                limg = tk.Label(new_window, image=new_image)
                limg.place(x=410,y=120)
            elif attempt.get() == 3:
                limg.pack_forget()
                bgimg = Image.open("/home/asiman/Pictures/3hangman.png")
                new_image = ImageTk.PhotoImage(bgimg)
                limg = tk.Label(new_window, image=new_image)
                limg.place(x=410,y=120)
            elif attempt.get() == 4:
                limg.pack_forget()
                bgimg = Image.open("/home/asiman/Pictures/4hang.png")
                new_image = ImageTk.PhotoImage(bgimg)
                limg = tk.Label(new_window, image=new_image)
                limg.place(x=410,y=120)
            elif attempt.get() == 5:
                limg.pack_forget()
                bgimg = Image.open("/home/asiman/Pictures/hang.png")
                new_image = ImageTk.PhotoImage(bgimg)
                limg = tk.Label(new_window, image=new_image)
                limg.place(x=410,y=120)
            elif attempt.get() == 6:
                limg.pack_forget()
                bgimg = Image.open("/home/asiman/Pictures/hanglast.png")
                new_image = ImageTk.PhotoImage(bgimg)
                limg = tk.Label(new_window, image=new_image)
                limg.place(x=410,y=120)
                new_window.after(1000, lambda nickname=nickname: lose(nickname))


                label_word_final =""
                for i in selected_word:
                    k = " "+i
                    label_word_final = label_word_final + k                                      
                
                Label = tk.Label(new_window, text=label_word_final, font=('Helvetica 30 bold'),fg = "green", bg='#b3e9d1')
                Label.place(x= 60,y=55)  
   
    button_PlayGame1= tk.Button(new_window, text='A', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command=lambda: [ClickLetter('A', selected_word), click_music()])
    button_PlayGame1.place(x=40,y=130)

    button_PlayGame2= tk.Button(new_window, text='B', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command= lambda:[ ClickLetter('B',selected_word), click_music()])
    button_PlayGame2.place(x=130,y=130)

    button_PlayGame3= tk.Button(new_window, text='C', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command=lambda: [ClickLetter('C',selected_word), click_music()])
    button_PlayGame3.place(x=220,y=130)

    button_PlayGame= tk.Button(new_window, text='D', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command=lambda:  [ClickLetter('D',selected_word), click_music()])
    button_PlayGame.place(x=310,y=130)

    button_PlayGame= tk.Button(new_window, text='E', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command=lambda:  [ClickLetter('E',selected_word), click_music()])
    button_PlayGame.place(x=40,y=180)

    button_PlayGame= tk.Button(new_window, text='F', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command= lambda: [ClickLetter('F',selected_word), click_music()])
    button_PlayGame.place(x=130,y=180)

    button_PlayGame= tk.Button(new_window, text='G', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command= lambda: [ClickLetter('G',selected_word), click_music()])
    button_PlayGame.place(x=220,y=180)

    button_PlayGame= tk.Button(new_window, text='H', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command= lambda: [ClickLetter('H',selected_word), click_music()])
    button_PlayGame.place(x=310,y=180)

    button_PlayGame= tk.Button(new_window, text='I', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command= lambda: [ClickLetter('I',selected_word), click_music()])
    button_PlayGame.place(x=310,y=230)

    button_PlayGame= tk.Button(new_window, text='J', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command=lambda:  [ClickLetter('J',selected_word), click_music()])
    button_PlayGame.place(x=40,y=230)

    button_PlayGame= tk.Button(new_window, text='K', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command= lambda: [ClickLetter('K',selected_word), click_music()])
    button_PlayGame.place(x=130,y=230)

    button_PlayGame= tk.Button(new_window, text='L', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command= lambda: [ClickLetter('L',selected_word), click_music()])
    button_PlayGame.place(x=220,y=230)

    button_PlayGame= tk.Button(new_window, text='M', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command=lambda:  [ClickLetter('M',selected_word), click_music()])
    button_PlayGame.place(x=40,y=280)

    button_PlayGame= tk.Button(new_window, text='N', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command= lambda: [ClickLetter('N',selected_word), click_music()])
    button_PlayGame.place(x=130,y=280)

    button_PlayGame= tk.Button(new_window, text='O', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command= lambda:[ ClickLetter('O',selected_word), click_music()])
    button_PlayGame.place(x=220,y=280)

    button_PlayGame= tk.Button(new_window, text='P', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command= lambda: [ClickLetter('P',selected_word), click_music()])
    button_PlayGame.place(x=310,y=280)
    
    button_PlayGame= tk.Button(new_window, text='Q', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command=lambda:  [ClickLetter('Q',selected_word), click_music()])
    button_PlayGame.place(x=40,y=330)

    button_PlayGame= tk.Button(new_window, text='R', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command= lambda:[ClickLetter('R',selected_word), click_music()])
    button_PlayGame.place(x=130,y=330)

    button_PlayGame= tk.Button(new_window, text='S', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command= lambda: [ClickLetter('S',selected_word), click_music()])
    button_PlayGame.place(x=220,y=330)

    button_PlayGame= tk.Button(new_window, text='T', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command= lambda: [ClickLetter('T',selected_word), click_music()])
    button_PlayGame.place(x=310,y=330)

    button_PlayGame= tk.Button(new_window, text='U', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command=lambda:  [ClickLetter('U',selected_word), click_music()])
    button_PlayGame.place(x=40,y=380)

    button_PlayGame= tk.Button(new_window, text='V', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command= lambda: [ClickLetter('V',selected_word), click_music()])
    button_PlayGame.place(x=130,y=380)

    button_PlayGame= tk.Button(new_window, text='W', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command=lambda:  [ClickLetter('W',selected_word), click_music()])
    button_PlayGame.place(x=220,y=380)

    button_PlayGame= tk.Button(new_window, text='X', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command= lambda: [ClickLetter('X',selected_word), click_music()])
    button_PlayGame.place(x=310,y=380)

    button_PlayGame= tk.Button(new_window, text='Y', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command= lambda: [ClickLetter('Y',selected_word), click_music()])
    button_PlayGame.place(x=40,y=430)

    button_PlayGame= tk.Button(new_window, text='Z', font = 'Helvetica 20 bold', width=3, bd =3,fg ="#257c65",bg = "white" , command= lambda: [ClickLetter('Z',selected_word), click_music()])
    button_PlayGame.place(x=130,y=430)

    new_window.mainloop()


label_Welcome = tk.Label(text = "Welcome to Hangman Game!",font = 'Times 30  bold',bg='#b3e9d1')
label_Welcome.place(x=120,y=30)

label_nickname = tk.Label(text = "Nickname:",font = 'Times 24 ')
label_nickname.place(x=400,y=100)

entry_nickname = tk.Entry(width=15, font = 'Helvetica 24 ')
entry_nickname.place(x=400,y=150)

button_PlayGame= tk.Button(window, text='Play', font = 'Helvetica 30  bold',bd =4, width=15, command= lambda: [click_music(),PlayGame()])
button_PlayGame.place(x=400,y=250)

window.mainloop()



