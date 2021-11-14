import flask
import paho.mqtt.client as mqtt
import json,ssl
app = flask.Flask(__name__)
def on_connect(client, userdata, rc):
    print("connected with result code", rc)

@app.route("/")
def helloWorld():
    return "Hello World"

@app.route("/uplink",methods=["POST"])
def uplink():
    json_data = flask.request.json
    data = json.loads(json_data["objectJSON"])
    token = data.get("token")
    if (token is not None):
        data.pop("token")
        #token = flask.request.headers.get('X-Authorization')
        print(token)
        client = mqtt.Client()
        client.username_pw_set(username=token,password=token)
        client.tls_set(cert_reqs=ssl.CERT_NONE,tls_version=ssl.PROTOCOL_TLSv1_2)
        client.tls_insecure_set(True)
        client.on_connect = on_connect
        #data = json.loads(json_data["objectJSON"])["DecodeDataHex"]
        #process_data = {"DeviceType": int(data[:2]),"Temp": int(data[2:6], 16)/100,
        #                "Humid": int(data[6:10],16)/100, "PM25": int(data[10:14],16)}
        #process_data = {"battery": float(data["battery"].replace("V",""))}
        #print(process_data)
        client.connect("mqtt.thingcontrol.io",8883, 60)
        client.publish("v1/devices/me/telemetry",payload=json.dumps(data), qos=0, retain=False)
        client.disconnect()
        return "OK"
    else:
        flask.abort(400)