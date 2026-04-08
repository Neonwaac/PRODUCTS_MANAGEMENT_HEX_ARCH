from src.config.mongo_connection import get_mongo_connection
from src.config.mysql_connection import get_mysql_connection
from bson import ObjectId
import re


class ProductoMysql:

  @staticmethod
  def leer_productos():
    connection = get_mysql_connection()
    try:
      with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM producto AS p ORDER BY p.idproducto")
        datos = cursor.fetchall()
      return datos
    finally:
      connection.close()

  @staticmethod
  def crear_producto(producto: str, marca: str, precio: float):
    connection = get_mysql_connection()
    try:
      with connection.cursor() as cursor:
        cursor.execute(
          "INSERT INTO producto (producto, marca, precio) VALUES (%s, %s, %s)",
          (producto, marca, precio),
        )
        connection.commit()
        return cursor.lastrowid
    finally:
      connection.close()

  @staticmethod
  def actualizar_producto(
    idproducto: int,
    producto: str,
    marca: str,
    precio: float,
  ):
    connection = get_mysql_connection()
    try:
      with connection.cursor() as cursor:
        cursor.execute(
          """
          UPDATE producto
          SET producto = %s, marca = %s, precio = %s
          WHERE idproducto = %s
          """,
          (producto, marca, precio, idproducto),
        )
        connection.commit()
        return cursor.rowcount
    finally:
      connection.close()

  @staticmethod
  def eliminar_producto(idproducto: int):
    connection = get_mysql_connection()
    try:
      with connection.cursor() as cursor:
        cursor.execute(
          "DELETE FROM producto WHERE idproducto = %s",
          (idproducto,),
        )
        connection.commit()
        return cursor.rowcount
    finally:
      connection.close()


class ImagenProductoMongo:

  @staticmethod
  def leer_imagenes():
    db = get_mongo_connection()
    imagenes = list(db.producto.aggregate([
      {
        "$project": {
          "_id": {
            "$toString": "$_id"
          },
          "producto": 1,
          "descripcion": 1,
          "url": 1,
          "mysql_id": 1,
        }
      }
    ]))

    return imagenes

  @staticmethod
  def crear_imagen(
    producto: str,
    descripcion: str,
    url: str,
    mysql_id: int | None = None,
  ):
    db = get_mongo_connection()
    payload = {
      "producto": producto,
      "descripcion": descripcion,
      "url": url,
    }
    if mysql_id is not None:
      payload["mysql_id"] = mysql_id

    resultado = db.producto.insert_one(payload)
    return str(resultado.inserted_id)

  @staticmethod
  def actualizar_imagen(
    idmongo: str,
    producto: str,
    descripcion: str,
    url: str,
    mysql_id: int | None = None,
  ):
    db = get_mongo_connection()
    payload = {
      "producto": producto,
      "descripcion": descripcion,
      "url": url,
    }
    if mysql_id is not None:
      payload["mysql_id"] = mysql_id
    else:
      payload["mysql_id"] = None

    resultado = db.producto.update_one(
      {"_id": ObjectId(idmongo)},
      {"$set": payload},
    )
    return resultado.modified_count

  @staticmethod
  def eliminar_imagen(idmongo: str):
    db = get_mongo_connection()
    resultado = db.producto.delete_one({"_id": ObjectId(idmongo)})
    return resultado.deleted_count

  @staticmethod
  def eliminar_imagen_por_mysql_id(mysql_id: int):
    db = get_mongo_connection()
    resultado = db.producto.delete_many({"mysql_id": mysql_id})
    return resultado.deleted_count

  @staticmethod
  def eliminar_imagen_por_producto(producto: str):
    db = get_mongo_connection()
    patron = f"^{re.escape(producto)}$"
    resultado = db.producto.delete_many({"producto": {"$regex": patron, "$options": "i"}})
    return resultado.deleted_count

  @staticmethod
  def leer_imagenes_por_mysql_id():
    db = get_mongo_connection()
    imagenes = list(db.producto.find(
      {"mysql_id": {"$exists": True, "$ne": None}},
      {
        "_id": 0,
        "mysql_id": 1,
        "producto": 1,
        "descripcion": 1,
        "url": 1,
      },
    ))
    return imagenes

  @staticmethod
  def upsert_imagen_por_mysql_id(
    mysql_id: int,
    producto: str,
    descripcion: str,
    url: str,
  ):
    db = get_mongo_connection()
    resultado = db.producto.update_one(
      {"mysql_id": mysql_id},
      {
        "$set": {
          "producto": producto,
          "descripcion": descripcion,
          "url": url,
          "mysql_id": mysql_id,
        }
      },
      upsert=True,
    )
    return {
      "matched": resultado.matched_count,
      "modified": resultado.modified_count,
      "upserted_id": str(resultado.upserted_id) if resultado.upserted_id else None,
    }
