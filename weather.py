from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)


def getweather():
    city = textfield.get()

    if not city.strip():
        messagebox.showerror("Weather App", "Please enter a city name!")
        return

    try:
        # Geolocation
        geolocator = Nominatim(user_agent="geoapiExercise")
        location = geolocator.geocode(city)
        if not location:
            raise ValueError("Invalid city name")
        
        # Timezone
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        if not result:
            raise ValueError("Could not determine timezone")

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")

        # Fetch weather data
        api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=3f2fe23091e55557e4764c90a7fab689"
        json_data = requests.get(api).json()

        if json_data.get("cod") != 200:
            raise ValueError(json_data.get("message", "Error fetching weather data"))

        condition = json_data['weather'][0]['main']
        description = json_data['weather'][0]['description']
        temp = int(json_data['main']['temp'] - 273.15)  # Convert Kelvin to Celsius
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']

        # Update labels with fetched data
        t.config(text=f"{temp}°C")
        c.config(text=f"{condition} | FEELS LIKE {temp}°C")
        w.config(text=f"{wind} m/s")
        h.config(text=f"{humidity}%")
        d.config(text=f"{description}")
        p.config(text=f"{pressure} hPa")

    except ValueError as ve:
        messagebox.showerror("Weather App", f"Error: {ve}")
    except Exception as e:
        messagebox.showerror("Weather App", f"Unable to fetch data: {e}")


# Search box
Search_image = PhotoImage(file="Search.png")
myimage = Label(image=Search_image)
myimage.place(x=20, y=20)

textfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

Search_icon = PhotoImage(file="Search_icon.png")
search_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getweather)
search_icon.place(x=400, y=34)

# Logo
logo_image = PhotoImage(file="logo.png")
logo = Label(image=logo_image)
logo.place(x=150, y=100)

# Bottom box
Frame_image = PhotoImage(file="box.png")
frame_myimage = Label(image=Frame_image)
frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

# Time and weather
name = Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(root, font=("helvetica", 20))
clock.place(x=30, y=130)

# Labels for weather details
label1 = Label(root, text="WIND", font=("Helvetica", 15, 'bold'), fg="white", bg="#add8e6")
label1.place(x=120, y=400)

label2 = Label(root, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fg="white", bg="#add8e6")
label2.place(x=250, y=400)

label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, 'bold'), fg="white", bg="#add8e6")
label3.place(x=430, y=400)

label4 = Label(root, text="PRESSURE", font=("Helvetica", 15, 'bold'), fg="white", bg="#add8e6")
label4.place(x=650, y=400)

# Dynamic data fields
t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)

c = Label(font=("arial", 15, "bold"))
c.place(x=400, y=250)

w = Label(text="...", font=("arial", 20, "bold"), bg="#add8e6")
w.place(x=120, y=430)

h = Label(text="...", font=("arial", 20, "bold"), bg="#add8e6")
h.place(x=280, y=430)

d = Label(text="...", font=("arial", 20, "bold"), bg="#add8e6")
d.place(x=450, y=430)

p = Label(text="...", font=("arial", 20, "bold"), bg="#add8e6")
p.place(x=670, y=430)

root.mainloop()
