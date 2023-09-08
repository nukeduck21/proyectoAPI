from flask import Flask, render_template, request, flash, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore, auth

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto por una clave secreta

# Configura Firebase Admin SDK
cred = credentials.Certificate("api-imc-firebase-adminsdk-f3xab-4321a2ccf0.json")
firebase_admin.initialize_app(cred)

# Inicializa Firestore
db = firestore.client()

# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']  # Obtén la contraseña del formulario

        # Determina el mensaje según el IMC
        imc = float(request.form['imc'])
        if imc < 18.5:
            message = 'Estás delgado.'
        elif imc >= 18.5 and imc < 25:
            message = 'Estás en forma.'
        else:
            message = 'Estás gordo.'

        try:
            # Crea un nuevo usuario en Firebase Authentication con la contraseña proporcionada
            user = auth.create_user(
                email=email,
                password=password
            )

            # Almacena el mensaje en Firestore
            user_ref = db.collection('users').document(user.uid)
            user_ref.set({
                'email': email,
                'imc': imc,
                'message': message
            })

            flash('Correo enviado con éxito', 'success')
        except Exception as e:
            flash('Error al crear el usuario: ' + str(e), 'error')

    return render_template('index.html')

if __name__ == '__main__':
    app.run()

