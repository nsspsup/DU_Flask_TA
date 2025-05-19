from flask import Flask, request, jsonify, render_template
import fnmatch
app = Flask(__name__)


trips = [{"id": 1, "destination": "Paris, France", "price": 350},
         {"id": 2, "destination": "Rome, Italy", "price": 400},
         {"id": 3, "destination": "Lisabon, Portugal", "price": 450},
         {"id": 4, "destination": "Bogota, Columbia", "price": 830},
         {"id": 5, "destination": "Fucking, Austria", "price": 30},
         {"id": 6, "destination": "Valletta, Malta", "price": 380},]
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/trips', methods=['GET'])
def get_trips():
    return jsonify(trips)

@app.route('/trips/search')
def search():
    trip_id = request.args.get('id', type=int)
    destination = request.args.get('destination', type=str)
    max_price = request.args.get('maxprice', type=int)

    filt_trips = trips

    if trip_id is not None:
        filt_trips = [trip for trip in filt_trips if trip['id'] == trip_id]
    if destination is not None:
        filt_trips = [trip for trip in filt_trips if fnmatch.fnmatch(trip['destination'].lower(), destination.lower() )]
    if max_price is not None:
        filt_trips = [trip for trip in filt_trips if trip['price'] >= max_price]

    return jsonify(filt_trips)


    return f"Searching for {query} with filter {filter}"
    #result = [trip for trip in trips if query in trip['destination'].lower()]

    #return jsonify(result)

@app.route('/book', methods=['POST'])
def book():
    data = request.get_json()
    matched_trip = next((trip for trip in trips if data['trip_id'] == trip['id']),None)
    if matched_trip is None:
        return f"Trip not found", 404
    else:
        return (f"Trip to {matched_trip['destination']} for {data['people']} "
                f"persons has been booked successfully for {data['name']}. ")




#table a html som generoval z gpt, lebo sa mi ti chcelo este trochu vypimpovat
@app.route('/table')
def trips_page():
    # Extract unique destinations for the dropdown
    destinations = sorted(set(trip['destination'] for trip in trips))

    # Get query parameters
    selected_destination = request.args.get('destination')
    max_price = request.args.get('price', type=int)

    # Filtering logic
    filtered_trips = trips

    if selected_destination:
        filtered_trips = [trip for trip in filtered_trips if trip['destination'] == selected_destination]

    if max_price is not None:
        filtered_trips = [trip for trip in filtered_trips if trip['price'] <= max_price]

    return render_template('table.html', trips=filtered_trips, destinations=destinations)

if __name__ == '__main__':
    app.run()
