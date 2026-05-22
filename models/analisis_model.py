from config.db import get_db


def obtener_perfil_usuario(usuario_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True, buffered=True)

    cursor.execute(
        """
        SELECT 
            p.*,
            u.username
        FROM perfil_usuario p
        INNER JOIN usuarios u ON p.usuario_id = u.id
        WHERE p.usuario_id = %s
        LIMIT 1
        """,
        (usuario_id,)
    )

    perfil = cursor.fetchone()

    cursor.close()
    conn.close()

    return perfil


def obtener_otros_perfiles(usuario_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT 
            p.*,
            u.username
        FROM perfil_usuario p
        INNER JOIN usuarios u ON p.usuario_id = u.id
        WHERE p.usuario_id != %s
        """,
        (usuario_id,)
    )

    perfiles = cursor.fetchall()

    cursor.close()
    conn.close()

    return perfiles


def obtener_progresos_usuario(usuario_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM progreso_usuario
        WHERE usuario_id = %s
        ORDER BY fecha ASC
        """,
        (usuario_id,)
    )

    progresos = cursor.fetchall()

    cursor.close()
    conn.close()

    return progresos


def obtener_comidas_usuario(usuario_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT 
            c.nombre,
            c.tipo,
            c.calorias,
            rc.cantidad,
            rc.calorias_totales
        FROM registro_comida rc
        INNER JOIN comidas c ON rc.comida_id = c.id
        WHERE rc.usuario_id = %s
        """,
        (usuario_id,)
    )

    comidas = cursor.fetchall()

    cursor.close()
    conn.close()

    return comidas


def obtener_rutinas_por_objetivo(objetivo):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM rutinas
        WHERE objetivo = %s
        """,
        (objetivo,)
    )

    rutinas = cursor.fetchall()

    cursor.close()
    conn.close()

    return rutinas