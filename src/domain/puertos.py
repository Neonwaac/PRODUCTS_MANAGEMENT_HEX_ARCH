from typing import Protocol


class RepositorioProducto(Protocol):

  def leer_productos(self):
    ...

  def crear_producto(self, producto: str, marca: str, precio: float):
    ...

  def actualizar_producto(
    self,
    idproducto: int,
    producto: str,
    marca: str,
    precio: float,
  ):
    ...

  def eliminar_producto(self, idproducto: int):
    ...


class RepositorioImagenProducto(Protocol):

  def leer_imagenes(self):
    ...

  def crear_imagen(
    self,
    producto: str,
    descripcion: str,
    url: str,
    mysql_id: int | None = None,
  ):
    ...

  def actualizar_imagen(
    self,
    idmongo: str,
    producto: str,
    descripcion: str,
    url: str,
    mysql_id: int | None = None,
  ):
    ...

  def eliminar_imagen(self, idmongo: str):
    ...

  def eliminar_imagen_por_mysql_id(self, mysql_id: int):
    ...

  def eliminar_imagen_por_producto(self, producto: str):
    ...

  def leer_imagenes_por_mysql_id(self):
    ...

  def upsert_imagen_por_mysql_id(
    self,
    mysql_id: int,
    producto: str,
    descripcion: str,
    url: str,
  ):
    ...
