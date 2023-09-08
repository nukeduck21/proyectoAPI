from flask import Flask, request, render_template
import firebase_admin
from firebase_admin import credentials, firestore

# Carga el archivo de credenciales de servicio
cred = credentials.Certificate("C:\\Users\\oscar\\PycharmProjects\\proyectoAPI\\api-imc-firebase-adminsdk-f3xab-4321a2ccf0.json")
firebase_admin.initialize_app(cred)


db = firestore.client()


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        imc = float(request.form['imc'])

        # Determina el mensaje según el IMC
        if imc < 18.5:
            message = 'Estás delgado.'
        elif imc >= 18.5 and imc < 25:
            message = 'Estás en forma.'
        else:
            message = 'Estás gordo.'

        # Guarda los datos en Firestore
        data = {
            'email': email,
            'imc': imc,
            'message': message
        }
        db.collection('usuarios').add(data)

        # Envía una respuesta al usuario
        return f'¡Tus datos se han guardado en Firestore! Tu IMC es {imc}.'

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


