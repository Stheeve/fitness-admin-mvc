from flask import Flask, render_template, session, redirect, url_for
from controllers.auth_controller import auth_bp
from controllers.rutina_controller import rutina_bp
from controllers.ejercicio_controller import ejercicio_bp
from controllers.rutina_ejercicio_controller import rutina_ejercicio_bp
from controllers.comida_controller import comida_bp
from controllers.perfil_controller import perfil_bp
from controllers.progreso_controller import progreso_bp
from controllers.registro_comida_controller import registro_comida_bp
from controllers.analisis_controller import analisis_bp

app = Flask(__name__)
app.secret_key = "clave_secreta_fitness"

app.register_blueprint(auth_bp)
app.register_blueprint(rutina_bp)
app.register_blueprint(ejercicio_bp)
app.register_blueprint(rutina_ejercicio_bp)
app.register_blueprint(comida_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(progreso_bp)
app.register_blueprint(registro_comida_bp)
app.register_blueprint(analisis_bp)

@app.route("/dashboard")
def dashboard():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("rol") == "admin":
        return render_template("dashboard_admin.html")

    return render_template("dashboard_usuario.html")
if __name__ == "__main__":
    app.run(debug=True)