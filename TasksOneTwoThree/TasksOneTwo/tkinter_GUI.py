import tkinter as tk

from get_info import Weather

cities_data = []
NUMBER_OF_CITIES = 5


def on_submit():
    city = input_city_entry.get()
    weather_forecast = Weather(city)
    result = weather_forecast.get_weather_info()
    result_label.config(
        text=f'City = {result["name"]}\ndescription = {result["weather"][0]["description"]}\ntemperature = {result["main"]["temp"]} °C'
        f'\nhumidity = {result["main"]["humidity"]}%'
    )
    cities_data.append({"city": result["name"], "temperature": result["main"]["temp"]})
    stats_data_label.config(text="")
    input_city_entry.delete(0, tk.END)
    if len(cities_data) == NUMBER_OF_CITIES:
        return stats()


def stats(city=None):
    if not city:
        coldest_city = min(cities_data, key=lambda x: x["temperature"])["city"]
        average_temperature = f'{sum([city["temperature"] for city in cities_data]) / len(cities_data):.2f}'
        stats_data_label.config(
            text=f"Coldest city = {coldest_city}\n Average temperature = {average_temperature} °C"
        )
        result_label.config(text="")
    else:
        pass


root = tk.Tk()

input_city_label = tk.Label(root, text="Enter city (in English): ", font=12)
input_city_label.pack()

input_city_entry = tk.Entry(root, width=30, font=12, border=10)
input_city_entry.pack()

submit_button = tk.Button(root, text="Submit", command=on_submit, fg="blue")
submit_button.pack()

result_label = tk.Label(root, text="", font=12)
result_label.pack()

stats_data_button = tk.Button(root, text="Stats", command=stats, fg="red")
stats_data_button.pack()

result_label = tk.Label(root, text="", font=12)
result_label.pack()

result_stats = tk.Label(root, text="", font=12)
result_stats.pack()

stats_data_label = tk.Label(root, text="", font=12)
stats_data_label.pack()

root.mainloop()
