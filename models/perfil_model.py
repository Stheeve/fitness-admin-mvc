from config.db import get_db


def obtener_perfil_por_usuario(usuario_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True, buffered=True)

    cursor.execute(
        "SELECT * FROM perfil_usuario WHERE usuario_id = %s LIMIT 1",
        (usuario_id,)
    )

    perfil = cursor.fetchone()

    cursor.close()
    conn.close()

    return perfil


def crear_perfil(usuario_id, edad, peso, altura, contextura, nivel_actividad, objetivo):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO perfil_usuario 
        (usuario_id, edad, peso, altura, contextura, nivel_actividad, objetivo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (usuario_id, edad, peso, altura, contextura, nivel_actividad, objetivo)
    )

    conn.commit()
    cursor.close()
    conn.close()


def actualizar_perfil(usuario_id, edad, peso, altura, contextura, nivel_actividad, objetivo):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE perfil_usuario
        SET edad = %s, peso = %s, altura = %s, contextura = %s,
            nivel_actividad = %s, objetivo = %s
        WHERE usuario_id = %s
        """,
        (edad, peso, altura, contextura, nivel_actividad, objetivo, usuario_id)
    )

    conn.commit()
    cursor.close()
    conn.close()
    
    
def actualizar_peso_perfil(usuario_id, nuevo_peso):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE perfil_usuario
        SET peso = %s
        WHERE usuario_id = %s
        """,
        (nuevo_peso, usuario_id)
    )

    conn.commit()
    cursor.close()
    conn.close()