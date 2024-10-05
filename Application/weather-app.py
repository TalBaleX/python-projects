from tkinter import *
from pyowm import OWM
import pyowm.commons.exceptions
import string

owm = OWM('307721570e943da6dfc67af435724db4')
mgr = owm.weather_manager()

app = Tk()
app.title("Weather-App")
app.geometry("700x500")
app.resizable(False, False)

city=StringVar()

def color_set(object, color):
    for child in object.winfo_children():
        child.config(bg=color)
        for child_child in child.winfo_children():
            child_child.config(bg=color)

def search_page(app):
    page = Frame(app)
    page.place(x=0, y=0, relwidth=1, relheight=1)

    frame = Frame(page)
    frame.pack()

    text_input = Entry(frame, width=20, bg='white', bd=2, foreground='black', font="Arial 17", justify="center",
                       textvariable=city)
    text_input.pack(side=LEFT, padx=10)
    btn = Button(frame, text="Get", bg="white", command=lambda: changepage())
    btn.pack(side=LEFT, padx=10)

    lbl = Label(page, text='Hi! Where it goes today?', font="Helvetica 32")
    lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

    color_set(app, "#60A9FF")

def weather_page(app):
    global city

    page = Frame(app)
    page.place(x=0, y=0, relwidth=1, relheight=1)

    frame = Frame(page)
    frame.pack()

    text_input = Entry(frame, width=20, bg='white', bd=2, foreground='black', font="Arial 17", justify="center",
                       textvariable=city)
    text_input.pack(side=LEFT, padx=10)
    btn = Button(frame, text="Get", bg="white", command=lambda: changepage())
    btn.pack(side=LEFT, padx=10)

    try:
        observation = mgr.weather_at_place(city.get())
        w = observation.weather

        temp_lbl = Label(page, text=f"{string.capwords(city.get())}\n{round(w.temperature('celsius')['temp'])}°C",
                         font="Helvetica 48")
        temp_lbl.place(relx=0.5, rely=0.25, anchor=CENTER)

        wind_lbl = Label(page, text=f"Wind: {round(w.wind()['speed'])} m/s", font="Helvetica 30")
        wind_lbl.place(relx=0.5, rely=0.55, anchor=CENTER)

        humidity_lbl = Label(page, text=f"Humidity: {round(w.humidity)}%", font="Helvetica 30")
        humidity_lbl.place(relx=0.5, rely=0.70, anchor=CENTER)

        clouds_lbl = Label(page, text=f"Clouds: {round(w.clouds)} oktas", font="Helvetica 30")
        clouds_lbl.place(relx=0.5, rely=0.85, anchor=CENTER)

        w = str(w).lower()

        if 'rain' in w:
            page.configure(bg='#3F66CB')
        elif 'clear' in w:
            page.configure(bg='#ECD71A')
        elif 'cloud' in w:
            page.configure(bg='#BEBEBE')
        elif 'mist' or 'haze' in w:
            page.configure(bg='#323842')
        else:
            page.configure(bg="#60A9FF")

    except pyowm.commons.exceptions.NotFoundError:
        page.configure(bg="#60A9FF")
        lbl = Label(page, text="Sorry, we didn't find anything", font="Helvetica 32")
        lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

    except pyowm.commons.exceptions.InvalidSSLCertificateError:
        lbl = Label(page, text="Bitte, kauf dir mal ja einen Router", font="Helvetica 32")
        lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

    color_set(app, page.cget("bg"))

def changepage():
    global app
    for widget in app.winfo_children():
        widget.destroy()

    weather_page(app)

search_page(app)

app.mainloop()