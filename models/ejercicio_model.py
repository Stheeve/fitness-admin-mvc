from config.db import get_db


def obtener_ejercicios():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM ejercicios")
    ejercicios = cursor.fetchall()

    cursor.close()
    conn.close()

    return ejercicios


def obtener_ejercicio_por_id(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM ejercicios WHERE id = %s", (id,))
    ejercicio = cursor.fetchone()

    cursor.close()
    conn.close()

    return ejercicio


def crear_ejercicio(nombre, tipo, calorias):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO ejercicios (nombre, tipo, calorias)
        VALUES (%s, %s, %s)
        """,
        (nombre, tipo, calorias)
    )

    conn.commit()
    cursor.close()
    conn.close()


def actualizar_ejercicio(id, nombre, tipo, calorias):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE ejercicios
        SET nombre = %s, tipo = %s, calorias = %s
        WHERE id = %s
        """,
        (nombre, tipo, calorias, id)
    )

    conn.commit()
    cursor.close()
    conn.close()


def eliminar_ejercicio(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM ejercicios WHERE id = %s", (id,))

    conn.commit()
    cursor.close()
    conn.close()