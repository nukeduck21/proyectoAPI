from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app, auth

# Inicializa la aplicación Flask
app = Flask(__name__)

# Configura Firebase
cred = credentials.Certificate("C:\\Users\\oscar\\PycharmProjects\\proyectoAPI\\api-imc-firebase-adminsdk-f3xab-4321a2ccf0.json")
firebase_app = initialize_app(cred)
db = firestore.client()

# Ruta principal
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

        # Crea un nuevo usuario en Firebase Authentication
        user = auth.create_user(
            email=email,
            password='password'  # Cambia esto por una contraseña segura
        )

        # Agrega el resultado a Firestore
        user_ref = db.collection('usuarios').document(user.uid)
        user_ref.set({
            'email': email,
            'imc': imc,
            'mensaje': message
        })

        # Envía una respuesta al correo del usuario
        # (Debes implementar esta parte utilizando un servicio de correo)

    return render_template('index.html')

if __name__ == '__main__':
    app.run()


