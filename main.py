from tkinter import *
from tkinter import Button, Label
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

def index():
    index_num = random.randint(0, len(data_list["French"]) - 1)
    return index_num


def next_card(button_pressed):
    global index_number, flip_card
    index_number = index()
    window.after_cancel(flip_card)
    canvas.itemconfig(image_create, image=photo)
    canvas.itemconfig(palabra, text=data_list["French"][index_number], fill="black")
    canvas.itemconfig(titulo, text="French", fill="black")
    flip_card = window.after(3000, change2english)
    print(button_pressed)
    if button_pressed is True:
        try:
            with open("words_to_learn.csv", "a") as wtl:
                wtl.write(f"{data_list["French"][index_number]},{data_list["English"][index_number]}\n")
        except FileNotFoundError:
            with open("words_to_learn.csv", "w") as wtl:
                wtl.write(f"{data_list["French"][index_number]},{data_list["English"][index_number]}\n")

def change2english():
    canvas.itemconfig(image_create, image=photoBack)
    canvas.itemconfig(palabra, text=data_list["English"][index_number], fill="white")
    canvas.itemconfig(titulo, text="English", fill="white")


#Invoco Pandas para abrir y leer un CSV
data = pandas.read_csv("data/french_words.csv")



#Convierto la columna de English a lista
data_list = data.to_dict("list")
print(data_list)

#Reviso si hay fichero "words_to_learn.csv" Si lo hay, leerlo, si no, crearlo
try:
    data_wtl = pandas.read_csv("words_to_learn.csv", encoding='latin-1')
    data_wtl_dict = data_wtl.to_dict("list")
    print(data_wtl_dict)
except FileNotFoundError:
    with open("words_to_learn.csv", "w") as wtl:
        wtl.write("French,English\n")
    data_wtl = pandas.read_csv("words_to_learn.csv", encoding='latin-1')
    data_wtl_dict = data_wtl.to_dict("list")

#recorremos el diccionario wtl y buscamos en el diccionario original para remover las palabras que ya sabemos

list_new_french = []

for v in data_list["French"]:
    for v2 in data_wtl_dict["French"]:
        if v != v2:
            list_new_french.append(v)

print(list_new_french)



#Ejemplo de como iterar en 2 dictionaries
# for (k, v), (k2, v2) in zip(data_wtl_dict.items(), data_wtl_dict.items()):
#     if (k, v) == (k2, v2):
#         print((k, v), (k2, v2))
#



#Crea ventana de programa
window = Tk()
window.title("Flash Card")
window.config(padx=10, pady=10, bg=BACKGROUND_COLOR)

#Crea objeto canvas para colocar imagenes o textos dentro
canvas = Canvas(width=1000, height=600, bg=BACKGROUND_COLOR, highlightthickness=0)
photo = PhotoImage(file="images/card_front.png")
photoBack = PhotoImage(file="images/card_back.png")
image_create = canvas.create_image(500, 300, image=photo)

####Genero 2 etiquetas que iran dentro del canvas
titulo = canvas.create_text(500, 150, text="title", font=("Arial", 40, "italic"))
palabra = canvas.create_text(500, 263, text="word", font=("Arial", 60, "bold"))

##Con las imagenes del folder creo 2 botones
ok = PhotoImage(file="images/right.png")
wrong = PhotoImage(file="images/wrong.png")
ok_button = Button(image=ok, highlightthickness=0, command=lambda: next_card(True))
wrong_button = Button(image=wrong, highlightthickness=0, command=lambda: next_card(False))

#####Acomodo los objetos en el GRID
canvas.grid(column=0, row=0, columnspan=2)
ok_button.grid(column=0, row=1)
wrong_button.grid(column=1, row=1)

index_number = index()

canvas.itemconfig(titulo, text="French")
canvas.itemconfig(palabra, text=data_list["French"][index_number])

flip_card = window.after(3000, change2english)
window.mainloop()

