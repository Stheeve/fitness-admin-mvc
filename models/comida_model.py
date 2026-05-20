from config.db import get_db


def obtener_comidas():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM comidas")
    comidas = cursor.fetchall()

    cursor.close()
    conn.close()

    return comidas


def obtener_comida_por_id(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM comidas WHERE id = %s", (id,))
    comida = cursor.fetchone()

    cursor.close()
    conn.close()

    return comida


def crear_comida(nombre, tipo, calorias, proteinas, carbohidratos, grasas):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO comidas (nombre, tipo, calorias, proteinas, carbohidratos, grasas)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (nombre, tipo, calorias, proteinas, carbohidratos, grasas)
    )

    conn.commit()
    cursor.close()
    conn.close()


def actualizar_comida(id, nombre, tipo, calorias, proteinas, carbohidratos, grasas):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE comidas
        SET nombre = %s, tipo = %s, calorias = %s, proteinas = %s, carbohidratos = %s, grasas = %s
        WHERE id = %s
        """,
        (nombre, tipo, calorias, proteinas, carbohidratos, grasas, id)
    )

    conn.commit()
    cursor.close()
    conn.close()


def eliminar_comida(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM comidas WHERE id = %s", (id,))

    conn.commit()
    cursor.close()
    conn.close()