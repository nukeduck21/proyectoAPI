import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa Firebase App
cred = credentials.Certificate("ruta/a/tu/credencial-de-servicio.json")
firebase_admin.initialize_app(cred)

# Configura el cliente de Firestore
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


