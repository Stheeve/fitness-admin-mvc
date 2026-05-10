from flask import Flask, render_template, session, redirect, url_for
from controllers.auth_controller import auth_bp
from controllers.rutina_controller import rutina_bp

app = Flask(__name__)
app.secret_key = "clave_secreta_fitness"

app.register_blueprint(auth_bp)
app.register_blueprint(rutina_bp)


@app.route("/dashboard")
def dashboard():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)