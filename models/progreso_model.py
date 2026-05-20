from config.db import get_db


def obtener_progresos_por_usuario(usuario_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT * FROM progreso_usuario
        WHERE usuario_id = %s
        ORDER BY fecha DESC
        """,
        (usuario_id,)
    )

    progresos = cursor.fetchall()

    cursor.close()
    conn.close()

    return progresos


def crear_progreso(usuario_id, fecha, peso_actual, porcentaje_grasa, observacion):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO progreso_usuario 
        (usuario_id, fecha, peso_actual, porcentaje_grasa, observacion)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (usuario_id, fecha, peso_actual, porcentaje_grasa, observacion)
    )

    conn.commit()
    cursor.close()
    conn.close()


def eliminar_progreso(id, usuario_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM progreso_usuario WHERE id = %s AND usuario_id = %s",
        (id, usuario_id)
    )

    conn.commit()
    cursor.close()
    conn.close()