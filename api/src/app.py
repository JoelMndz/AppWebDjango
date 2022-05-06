from flask import Flask, request
from src.controlador import solicitud, consulta, calsificacionFecha

app = Flask(__name__)

@app.route('/solicitud',methods=["POST"])
def rutaSolicitud():
  data = solicitud(request)
  return data

@app.route('/consulta',methods=["GET"])
def rutaConsulta():
  data = consulta()
  return data

@app.route('/clasificacion-fecha',methods=["POST"])
def ruta():
  calsificacionFecha(request.form['empresa'],request.form['fecha'])
  return request.form



if(__name__ == "__main__"):
  app.run(debug=True, port=5000)