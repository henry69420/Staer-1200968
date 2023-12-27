from flask import Flask, render_template, request, render_template_string
import folium
import sqlite3
import pycountry

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def map():

    all_countries = list(pycountry.countries)
    con = sqlite3.connect('opensky.db')
    cur = con.cursor()
    sql_query = ""

    if request.method == 'POST':
        country_filter = request.form.get('country_filter')
	 

        sql_query = "SELECT * FROM aircraft_state"
        if country_filter:
            sql_query += f" WHERE origin_country = '{country_filter}' LIMIT 100"


        
        cur.execute(sql_query)




  
        data = cur.fetchall()
        con.close()

   
        markers = []
        for record in data:
            icao24 = record[1]
            latitude = record[7]
            longitude = record[6]

            if latitude is not None and longitude is not None:
                markers.append((latitude, longitude, f"ICAO24: {icao24}"))

        
        filter_html = """
        <div id="filters">
            <form method="POST" action="/">
                <label for="country_filter">Filtrar por país:</label>
                <select name="country_filter" id="country_filter">
                    <option value="">Selecionar país</option>
        """
        for country in all_countries:
            filter_html += f"<option value='{country.name}'>{country.name}</option>\n"
        filter_html += """
                </select>
                <button type="submit">Aplicar Filtros</button>
            </form>
        </div>
        """

        
        my_map = folium.Map(location=[0, 0], zoom_start=2, width='100%', height='92%')
        for marker in markers:
            folium.Marker([marker[0], marker[1]], popup=marker[2]).add_to(my_map)
        my_map.get_root().html.add_child(folium.Element(filter_html))
        my_map.save('templates/map.html')

    return render_template('map.html', countries=all_countries)

if __name__ == '__main__':
    app.run(debug=True)