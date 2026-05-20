from flask import Flask, render_template, session, redirect, url_for
from controllers.auth_controller import auth_bp
from controllers.rutina_controller import rutina_bp
from controllers.ejercicio_controller import ejercicio_bp
from controllers.rutina_ejercicio_controller import rutina_ejercicio_bp
from controllers.comida_controller import comida_bp
from controllers.perfil_controller import perfil_bp

app = Flask(__name__)
app.secret_key = "clave_secreta_fitness"

app.register_blueprint(auth_bp)
app.register_blueprint(rutina_bp)
app.register_blueprint(ejercicio_bp)
app.register_blueprint(rutina_ejercicio_bp)
app.register_blueprint(comida_bp)
app.register_blueprint(perfil_bp)


@app.route("/dashboard")
def dashboard():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)