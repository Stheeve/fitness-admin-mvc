from config.db import get_db


def obtener_recomendacion_activa(usuario_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT 
            ru.id,
            ru.usuario_id,
            ru.rutina_id,
            ru.fecha_recomendacion,
            ru.estado,
            ru.resultado,
            ru.observacion,
            r.nombre AS rutina_nombre,
            r.descripcion AS rutina_descripcion,
            r.nivel,
            r.objetivo
        FROM recomendacion_usuario ru
        LEFT JOIN rutinas r ON ru.rutina_id = r.id
        WHERE ru.usuario_id = %s AND ru.estado = 'activa'
        ORDER BY ru.fecha_recomendacion DESC
        LIMIT 1
        """,
        (usuario_id,)
    )

    recomendacion = cursor.fetchone()

    cursor.close()
    conn.close()

    return recomendacion


def desactivar_recomendaciones(usuario_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE recomendacion_usuario
        SET estado = 'finalizada'
        WHERE usuario_id = %s AND estado = 'activa'
        """,
        (usuario_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()


def guardar_recomendacion(usuario_id, rutina_id, fecha_recomendacion, observacion):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO recomendacion_usuario 
        (usuario_id, rutina_id, fecha_recomendacion, estado, resultado, observacion)
        VALUES (%s, %s, %s, 'activa', NULL, %s)
        """,
        (usuario_id, rutina_id, fecha_recomendacion, observacion)
    )

    conn.commit()
    cursor.close()
    conn.close()
    
    
def actualizar_resultado_recomendacion(recomendacion_id, resultado, observacion):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE recomendacion_usuario
        SET resultado = %s, observacion = %s
        WHERE id = %s
        """,
        (resultado, observacion, recomendacion_id)
    )

    conn.commit()
    cursor.close()
    conn.close()
    
    
def obtener_ejercicios_recomendacion(usuario_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT 
            e.nombre AS ejercicio_nombre,
            e.tipo,
            e.calorias,
            re.series,
            re.repeticiones
        FROM recomendacion_usuario ru
        INNER JOIN rutina_ejercicio re ON ru.rutina_id = re.rutina_id
        INNER JOIN ejercicios e ON re.ejercicio_id = e.id
        WHERE ru.usuario_id = %s 
        AND ru.estado = 'activa'
        ORDER BY e.nombre
        """,
        (usuario_id,)
    )

    ejercicios = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return ejercicios


def obtener_ultima_recomendacion_no_funciono(usuario_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM recomendacion_usuario
        WHERE usuario_id = %s
        AND resultado = 'no funciono'
        ORDER BY id DESC
        LIMIT 1
        """,
        (usuario_id,)
    )

    recomendacion = cursor.fetchone()

    cursor.close()
    conn.close()

    return recomendacion


def obtener_rutinas_exitosas_usuario(usuario_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT 
            ru.rutina_id,
            r.nombre,
            r.descripcion,
            r.nivel,
            r.objetivo
        FROM recomendacion_usuario ru
        INNER JOIN rutinas r ON ru.rutina_id = r.id
        WHERE ru.usuario_id = %s
        AND ru.resultado = 'funciono'
        """,
        (usuario_id,)
    )

    rutinas = cursor.fetchall()

    cursor.close()
    conn.close()

    return rutinas