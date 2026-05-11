from config.db import get_db


def obtener_asignaciones():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            re.id,
            r.nombre AS rutina,
            e.nombre AS ejercicio,
            re.series,
            re.repeticiones
        FROM rutina_ejercicio re
        INNER JOIN rutinas r ON re.rutina_id = r.id
        INNER JOIN ejercicios e ON re.ejercicio_id = e.id
    """)

    asignaciones = cursor.fetchall()

    cursor.close()
    conn.close()

    return asignaciones


def crear_asignacion(rutina_id, ejercicio_id, series, repeticiones):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO rutina_ejercicio (rutina_id, ejercicio_id, series, repeticiones)
        VALUES (%s, %s, %s, %s)
        """,
        (rutina_id, ejercicio_id, series, repeticiones)
    )

    conn.commit()
    cursor.close()
    conn.close()


def eliminar_asignacion(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM rutina_ejercicio WHERE id = %s", (id,))

    conn.commit()
    cursor.close()
    conn.close()