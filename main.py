import pymongo
from flask import Flask, request, jsonify, json
app = Flask(__name__)

clientAddress = pymongo.MongoClient("mongodb://localhost:27017/")
DB = clientAddress["SOR-location"]
locationCollection = DB["location"]

#validate location data
def validateLocation(location_data):

   if type(location_data) != list:
      raise ValueError('{"Error": "Location must be an array of lon and lat"}')

   if len(location_data) != 2:
      raise ValueError('{"Error": "Recived location array array must be 2 long of lon lat"}')
   
   if isinstance(location_data[0], (int, float)) == False:
      raise ValueError('{"Error": "lon lat must be int or float"}')
   
   if isinstance(location_data[1], (int, float)) == False:
      raise ValueError('{"Error": "lon lat must be int or float"}')
   
   if -180 > location_data[0] > 180:
      raise ValueError('{"Error": "lon must be between -180 and 180"}')
   
   if -90 > location_data[0] > 90:
      raise ValueError('{"Error": "lat must be between -90 and 90"}')

def testLocation(location_data):
   return_data = []
   QueryData = locationCollection.find({"geometry":{
  "$nearSphere": {
    "$geometry": {
        "type" : "Point",
        "coordinates" : [location_data[1],location_data[0]]
     },
     "$maxDistance": 153
  }
}},{"_id":   0, "geometry":   0})
   
   for i in QueryData:
      return_data.append(i)
   
   if QueryData is None:
      x = {"Error": "Outside service area","province": "*c unknown"}
   return(return_data)


@app.route('/rest/sor', methods = ['POST', 'GET'])

def main_endpoint():         

   client_data = request.json
      
   try:
      validateLocation(client_data["location"])
      return testLocation(client_data["location"]), 200

   except KeyError:
      return jsonify({"Error": "Location data must be in all requests"}), 400
   
   except ValueError as e:
      return json.loads(str(e)), 400
   
   except:
      return jsonify({"Error":   "Unkown error has occured"}), 500      

if __name__ == '__main__':
   app.run(debug=False, port=5000, host='0.0.0.0')



#dr wimm 2 weeks cash. muviniy nuro

#208-