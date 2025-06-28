from flask import Flask, render_template
import csv
from collections import Counter

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html") 

@app.route("/tentang")
def tentang():
    return render_template("tentang.html")

@app.route("/kontak")
def kontak():
    return render_template("kontak.html")

@app.route("/data")
def data():
    data = []
    labels = []
    values = []
    usia_counter = Counter()
    with open("./static/data.csv", "r") as file:
        reader = csv.reader(file)
        headers = next(reader)        
        for line in file:
            name, age, city = line.strip().split(",")
            data.append({"name": name, "age": age, "city": city})
            labels.append(name)
            values.append(int(age))
            usia_counter[int(age)] += 1
    labels = list(usia_counter.keys())
    print(labels)
    values = list(usia_counter.values())
    return render_template("data.html", headers=headers, data=data, labels=labels, values=values)

if __name__ == "__main__":
    app.run(debug=True)
