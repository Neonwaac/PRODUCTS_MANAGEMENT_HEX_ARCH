from src.domain.puertos import RepositorioImagenProducto, RepositorioProducto
from decimal import Decimal, InvalidOperation
from urllib.parse import urlparse


def _validar_texto(valor: str, campo: str, minimo: int = 2, maximo: int = 120):
  texto = (valor or "").strip()
  if len(texto) < minimo or len(texto) > maximo:
    raise ValueError(f"El campo '{campo}' debe tener entre {minimo} y {maximo} caracteres")
  return texto


def _validar_precio(valor: str):
  try:
    precio = Decimal(str(valor))
  except (InvalidOperation, ValueError, TypeError):
    raise ValueError("El precio debe ser numerico")

  if precio < 0:
    raise ValueError("El precio no puede ser negativo")
  return float(precio)


def _validar_url(valor: str):
  url = (valor or "").strip()
  partes = urlparse(url)
  if not url or partes.scheme not in ("http", "https") or not partes.netloc:
    raise ValueError("La URL debe ser valida y comenzar por http:// o https://")
  return url


def _validar_mysql_id_opcional(valor: str | None):
  raw = (valor or "").strip()
  if not raw:
    return None
  if not raw.isdigit() or int(raw) <= 0:
    raise ValueError("El campo MySQL ID debe ser un numero entero positivo")
  return int(raw)


def validar_payload_producto(producto: str, marca: str, precio: str):
  return {
    "producto": _validar_texto(producto, "producto"),
    "marca": _validar_texto(marca, "marca"),
    "precio": _validar_precio(precio),
  }


def validar_payload_imagen(
  producto: str,
  descripcion: str,
  url: str,
  mysql_id: str | None,
):
  return {
    "producto": _validar_texto(producto, "producto"),
    "descripcion": _validar_texto(descripcion, "descripcion", minimo=3, maximo=200),
    "url": _validar_url(url),
    "mysql_id": _validar_mysql_id_opcional(mysql_id),
  }


def listar_productos(repositorio: RepositorioProducto):
  return repositorio.leer_productos()


def listar_imagenes(repositorio: RepositorioImagenProducto):
  return repositorio.leer_imagenes()


def crear_producto(
  repositorio: RepositorioProducto,
  producto: str,
  marca: str,
  precio: float,
):
  return repositorio.crear_producto(producto, marca, precio)


def actualizar_producto(
  repositorio: RepositorioProducto,
  idproducto: int,
  producto: str,
  marca: str,
  precio: float,
):
  return repositorio.actualizar_producto(idproducto, producto, marca, precio)


def eliminar_producto(repositorio: RepositorioProducto, idproducto: int):
  return repositorio.eliminar_producto(idproducto)


def crear_imagen(
  repositorio: RepositorioImagenProducto,
  producto: str,
  descripcion: str,
  url: str,
  mysql_id: int | None = None,
):
  return repositorio.crear_imagen(producto, descripcion, url, mysql_id)


def actualizar_imagen(
  repositorio: RepositorioImagenProducto,
  idmongo: str,
  producto: str,
  descripcion: str,
  url: str,
  mysql_id: int | None = None,
):
  return repositorio.actualizar_imagen(idmongo, producto, descripcion, url, mysql_id)


def eliminar_imagen(repositorio: RepositorioImagenProducto, idmongo: str):
  return repositorio.eliminar_imagen(idmongo)


def listar_productos_completos(
  repositorio_producto: RepositorioProducto,
  repositorio_imagen: RepositorioImagenProducto,
):
  productos_mysql = repositorio_producto.leer_productos()
  imagenes_mongo = repositorio_imagen.leer_imagenes()

  imagenes_por_id = {
    img["mysql_id"]: img
    for img in imagenes_mongo
    if img.get("mysql_id") is not None
  }

  imagenes_por_nombre = {
    str(img.get("producto", "")).strip().lower(): img
    for img in imagenes_mongo
    if img.get("producto")
  }

  data = []
  for producto in productos_mysql:
    mysql_id = producto["idproducto"]
    imagen = imagenes_por_id.get(mysql_id)
    if imagen is None:
      key_nombre = str(producto.get("producto", "")).strip().lower()
      imagen = imagenes_por_nombre.get(key_nombre)

    if imagen is None:
      continue

    data.append(
      {
        "idproducto": mysql_id,
        "producto": producto["producto"],
        "marca": producto["marca"],
        "precio": producto["precio"],
        "descripcion": imagen.get("descripcion", ""),
        "url": imagen.get("url", ""),
      }
    )

  return data


def crear_producto_completo(
  repositorio_producto: RepositorioProducto,
  repositorio_imagen: RepositorioImagenProducto,
  producto: str,
  marca: str,
  precio: float,
  descripcion: str,
  url: str,
):
  nuevo_id = repositorio_producto.crear_producto(producto, marca, precio)
  try:
    repositorio_imagen.crear_imagen(
      producto=producto,
      descripcion=descripcion,
      url=url,
      mysql_id=nuevo_id,
    )
    return nuevo_id
  except Exception:
    repositorio_producto.eliminar_producto(nuevo_id)
    raise


def actualizar_producto_completo(
  repositorio_producto: RepositorioProducto,
  repositorio_imagen: RepositorioImagenProducto,
  idproducto: int,
  producto: str,
  marca: str,
  precio: float,
  descripcion: str,
  url: str,
):
  repositorio_producto.actualizar_producto(idproducto, producto, marca, precio)
  repositorio_imagen.upsert_imagen_por_mysql_id(
    mysql_id=idproducto,
    producto=producto,
    descripcion=descripcion,
    url=url,
  )


def eliminar_producto_completo(
  repositorio_producto: RepositorioProducto,
  repositorio_imagen: RepositorioImagenProducto,
  idproducto: int,
):
  productos = repositorio_producto.leer_productos()
  producto_en_mysql = next((p for p in productos if p["idproducto"] == idproducto), None)

  eliminados_mongo = repositorio_imagen.eliminar_imagen_por_mysql_id(idproducto)
  if eliminados_mongo == 0 and producto_en_mysql:
    repositorio_imagen.eliminar_imagen_por_producto(producto_en_mysql["producto"])

  repositorio_producto.eliminar_producto(idproducto)
