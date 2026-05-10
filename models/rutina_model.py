from config.db import get_db


def obtener_rutinas():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM rutinas")
    rutinas = cursor.fetchall()

    cursor.close()
    conn.close()

    return rutinas


def obtener_rutina_por_id(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM rutinas WHERE id = %s", (id,))
    rutina = cursor.fetchone()

    cursor.close()
    conn.close()

    return rutina


def crear_rutina(nombre, descripcion, nivel, objetivo):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO rutinas (nombre, descripcion, nivel, objetivo)
        VALUES (%s, %s, %s, %s)
        """,
        (nombre, descripcion, nivel, objetivo)
    )

    conn.commit()
    cursor.close()
    conn.close()


def actualizar_rutina(id, nombre, descripcion, nivel, objetivo):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE rutinas
        SET nombre = %s, descripcion = %s, nivel = %s, objetivo = %s
        WHERE id = %s
        """,
        (nombre, descripcion, nivel, objetivo, id)
    )

    conn.commit()
    cursor.close()
    conn.close()


def eliminar_rutina(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM rutinas WHERE id = %s", (id,))

    conn.commit()
    cursor.close()
    conn.close()