from config.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash


def crear_usuario(username, password):
    conn = get_db()
    cursor = conn.cursor()

    password_hash = generate_password_hash(password)

    cursor.execute(
        "INSERT INTO usuarios (username, password) VALUES (%s, %s)",
        (username, password_hash)
    )

    conn.commit()
    cursor.close()
    conn.close()


def obtener_usuario_por_username(username):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM usuarios WHERE username = %s",
        (username,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    return usuario


def validar_usuario(username, password):
    usuario = obtener_usuario_por_username(username)

    if usuario and check_password_hash(usuario["password"], password):
        return usuario

    return None