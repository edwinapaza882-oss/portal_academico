from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash

app = Flask(__name__)
app.secret_key = 'clave_secreta_portal_academico'
usuarios = {
    "juan": "1234",
    "maria": "abcd",
    "pedro": "2026"
}

cursos_lista = [
    {"id": 1, "nombre": "Programación Web", "docente": "Luis Pérez", "cupos": 15},
    {"id": 2, "nombre": "Bases de Datos", "docente": "Ana López", "cupos": 8},
    {"id": 3, "nombre": "Inteligencia Artificial", "docente": "Carlos Rojas", "cupos": 0}
]

@app.route('/')
def index():
    usuario_cookie = request.cookies.get('usuario_preferido')
    return render_template('index.html', usuario_cookie=usuario_cookie)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        contrasena = request.form.get('contrasena')

        if usuario in usuarios and usuarios[usuario] == contrasena:
            session['usuario'] = usuario
            response = make_response(redirect(url_for('cursos_view')))
            response.set_cookie('usuario_preferido', usuario, max_age=60*60*24*30)
            return response
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/cursos')
def cursos_view():
    return render_template('cursos.html', cursos=cursos_lista)

@app.route('/perfil')
def perfil():
    if 'usuario' not in session:
        flash('Debes iniciar sesión para acceder a tu perfil.', 'danger')
        return redirect(url_for('login'))
    return render_template('perfil.html', usuario=session['usuario'])

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

@app.route('/eliminar_cookie')
def eliminar_cookie():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('usuario_preferido', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True)