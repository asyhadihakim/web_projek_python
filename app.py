from flask import Flask, render_template, request
import csv
from collections import Counter
import math

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html") 
    
@app.route():("/test")
def test():
    print("abc")

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

@app.route("/covid19")
def covid19():
    data = []
    labels = []
    values = []
    prov_counter = Counter()
    with open("./static/covid_19_indonesia_time_series_all.csv", "r") as file:
        reader = csv.reader(file)
        headers = next(reader)        
        for line in file:
            provinsi, total_cases, total_deaths, total_recovered, total_active_cases = line.strip().split(",")
            data.append({"provinsi": provinsi, "total_cases": total_cases, "total_deaths": total_deaths, "total_recovered": total_recovered, "total_active_cases": total_active_cases})
            labels.append(provinsi)
            values.append(int(total_cases))
            prov_counter[int(total_cases)] += 1


    labels = list(prov_counter.keys())
    values = list(prov_counter.values())
    return render_template("data_covid.html", headers=headers, data=data, labels=labels, values=values)

@app.route("/boston")
def boston():
    data = []
    labels = []
    values = []
    age_counter = Counter()

    # Ambil filter dari query string
    filter_country = request.args.get("country", "").lower()
    min_age = request.args.get("min_age")
    max_age = request.args.get("max_age")

    per_page = 10
    page = int(request.args.get("page", 1))
    with open("./static/Dataset-Boston-2019.csv", "r") as file:
        reader = csv.reader(file)
        headers = next(reader)        
        all_lines = list(reader)
        for line in all_lines:
            Rank_Tot,Age,Gender,Country,Result_hr,Result_sec,Rank_Gender,Country_code,*_ = line

            # Filter logika
            age_int = int(Age)
            if filter_country and filter_country not in Country.lower():
                continue
            if min_age and age_int < int(min_age):
                continue
            if max_age and age_int > int(max_age):
                continue

            data.append({"Ranking": Rank_Tot, "Age": Age, "Gender": Gender, "Country": Country,"Result_hr": Result_hr,"Result_sec": Result_sec,"Rank_Gender": Rank_Gender,"Country_code": Country_code})
            labels.append(Country)
            values.append(int(Age))
            age_counter[int(Age)] += 1
    
    #count the page
    total_data = len(data)
    total_pages = math.ceil(total_data / per_page)

    #data untuk halaman saat ini
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = data[start:end]

    labels = list(age_counter.keys())
    values = list(age_counter.values())
    return render_template("boston.html", headers=headers, data=paginated_data, labels=labels, values=values, current_page=page, total_pages=total_pages,filter_country=filter_country,
        min_age=min_age,
        max_age=max_age) 

if __name__ == "__main__":
    app.run(debug=True)
