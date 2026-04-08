from flask import Blueprint, flash, redirect, render_template, request, url_for

from src.application.casos_uso import (
  actualizar_imagen,
  actualizar_producto,
  actualizar_producto_completo,
  crear_imagen,
  crear_producto,
  crear_producto_completo,
  eliminar_imagen,
  eliminar_producto,
  eliminar_producto_completo,
  listar_imagenes,
  listar_productos,
  listar_productos_completos,
  validar_payload_imagen,
  validar_payload_producto,
)
from src.domain.puertos import RepositorioImagenProducto, RepositorioProducto


def crear_blueprint_productos(
  repositorio_producto: RepositorioProducto,
  repositorio_imagen: RepositorioImagenProducto,
):
  productos_c = Blueprint(
    'productos_c', __name__, template_folder='../templates'
  )

  @productos_c.route("/productos")
  def obtener_productos():
    data = listar_productos(repositorio_producto)
    return render_template("productos.html", data=data)

  @productos_c.route("/productos", methods=["POST"])
  def crear_producto_ruta():
    try:
      payload = validar_payload_producto(
        request.form.get("producto", ""),
        request.form.get("marca", ""),
        request.form.get("precio", ""),
      )
      crear_producto(
        repositorio_producto,
        payload["producto"],
        payload["marca"],
        payload["precio"],
      )
      flash("Producto creado correctamente", "success")
    except ValueError as ex:
      flash(str(ex), "danger")
    return redirect(url_for("productos_c.obtener_productos"))

  @productos_c.route("/productos/editar/<int:idproducto>", methods=["POST"])
  def editar_producto_ruta(idproducto: int):
    try:
      payload = validar_payload_producto(
        request.form.get("producto", ""),
        request.form.get("marca", ""),
        request.form.get("precio", ""),
      )
      actualizar_producto(
        repositorio_producto,
        idproducto,
        payload["producto"],
        payload["marca"],
        payload["precio"],
      )
      flash("Producto actualizado correctamente", "success")
    except ValueError as ex:
      flash(str(ex), "danger")
    return redirect(url_for("productos_c.obtener_productos"))

  @productos_c.route("/productos/eliminar/<int:idproducto>", methods=["POST"])
  def eliminar_producto_ruta(idproducto: int):
    eliminar_producto(repositorio_producto, idproducto)
    flash("Producto eliminado", "success")
    return redirect(url_for("productos_c.obtener_productos"))

  @productos_c.route("/imagenes_productos")
  def obtener_imagenes():
    data2 = listar_imagenes(repositorio_imagen)
    return render_template("imagenes_productos.html", data2=data2)

  @productos_c.route("/imagenes_productos", methods=["POST"])
  def crear_imagen_ruta():
    try:
      payload = validar_payload_imagen(
        request.form.get("producto", ""),
        request.form.get("descripcion", ""),
        request.form.get("url", ""),
        request.form.get("mysql_id", ""),
      )
      crear_imagen(
        repositorio_imagen,
        payload["producto"],
        payload["descripcion"],
        payload["url"],
        payload["mysql_id"],
      )
      flash("Imagen creada correctamente", "success")
    except ValueError as ex:
      flash(str(ex), "danger")
    return redirect(url_for("productos_c.obtener_imagenes"))

  @productos_c.route("/imagenes_productos/editar/<string:idmongo>", methods=["POST"])
  def editar_imagen_ruta(idmongo: str):
    try:
      payload = validar_payload_imagen(
        request.form.get("producto", ""),
        request.form.get("descripcion", ""),
        request.form.get("url", ""),
        request.form.get("mysql_id", ""),
      )
      actualizar_imagen(
        repositorio_imagen,
        idmongo,
        payload["producto"],
        payload["descripcion"],
        payload["url"],
        payload["mysql_id"],
      )
      flash("Imagen actualizada correctamente", "success")
    except ValueError as ex:
      flash(str(ex), "danger")
    return redirect(url_for("productos_c.obtener_imagenes"))

  @productos_c.route("/imagenes_productos/eliminar/<string:idmongo>", methods=["POST"])
  def eliminar_imagen_ruta(idmongo: str):
    eliminar_imagen(repositorio_imagen, idmongo)
    flash("Imagen eliminada", "success")
    return redirect(url_for("productos_c.obtener_imagenes"))

  @productos_c.route("/productos_completos")
  def obtener_productos_completos():
    data3 = listar_productos_completos(repositorio_producto, repositorio_imagen)
    return render_template("productos_completos.html", data3=data3)

  @productos_c.route("/productos_completos", methods=["POST"])
  def crear_producto_completo_ruta():
    try:
      payload_producto = validar_payload_producto(
        request.form.get("producto", ""),
        request.form.get("marca", ""),
        request.form.get("precio", ""),
      )
      payload_imagen = validar_payload_imagen(
        request.form.get("producto", ""),
        request.form.get("descripcion", ""),
        request.form.get("url", ""),
        None,
      )
      crear_producto_completo(
        repositorio_producto,
        repositorio_imagen,
        payload_producto["producto"],
        payload_producto["marca"],
        payload_producto["precio"],
        payload_imagen["descripcion"],
        payload_imagen["url"],
      )
      flash("Registro conjunto creado correctamente", "success")
    except ValueError as ex:
      flash(str(ex), "danger")
    return redirect(url_for("productos_c.obtener_productos_completos"))

  @productos_c.route(
    "/productos_completos/editar/<int:idproducto>",
    methods=["POST"],
  )
  def editar_producto_completo_ruta(idproducto: int):
    try:
      payload_producto = validar_payload_producto(
        request.form.get("producto", ""),
        request.form.get("marca", ""),
        request.form.get("precio", ""),
      )
      payload_imagen = validar_payload_imagen(
        request.form.get("producto", ""),
        request.form.get("descripcion", ""),
        request.form.get("url", ""),
        str(idproducto),
      )
      actualizar_producto_completo(
        repositorio_producto,
        repositorio_imagen,
        idproducto,
        payload_producto["producto"],
        payload_producto["marca"],
        payload_producto["precio"],
        payload_imagen["descripcion"],
        payload_imagen["url"],
      )
      flash("Registro conjunto actualizado correctamente", "success")
    except ValueError as ex:
      flash(str(ex), "danger")
    return redirect(url_for("productos_c.obtener_productos_completos"))

  @productos_c.route(
    "/productos_completos/eliminar/<int:idproducto>",
    methods=["POST"],
  )
  def eliminar_producto_completo_ruta(idproducto: int):
    eliminar_producto_completo(
      repositorio_producto,
      repositorio_imagen,
      idproducto,
    )
    flash("Registro eliminado en ambas bases", "success")
    return redirect(url_for("productos_c.obtener_productos_completos"))

  return productos_c






