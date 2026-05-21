from config.db import get_db


def obtener_registros_comida(usuario_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT 
            rc.id,
            rc.fecha,
            c.nombre AS comida,
            c.tipo,
            c.calorias,
            rc.cantidad,
            rc.calorias_totales
        FROM registro_comida rc
        INNER JOIN comidas c ON rc.comida_id = c.id
        WHERE rc.usuario_id = %s
        ORDER BY rc.fecha DESC
        """,
        (usuario_id,)
    )

    registros = cursor.fetchall()

    cursor.close()
    conn.close()

    return registros


def crear_registro_comida(usuario_id, comida_id, fecha, cantidad, calorias_totales):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO registro_comida 
        (usuario_id, comida_id, fecha, cantidad, calorias_totales)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (usuario_id, comida_id, fecha, cantidad, calorias_totales)
    )

    conn.commit()
    cursor.close()
    conn.close()


def eliminar_registro_comida(id, usuario_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM registro_comida WHERE id = %s AND usuario_id = %s",
        (id, usuario_id)
    )

    conn.commit()
    cursor.close()
    conn.close()