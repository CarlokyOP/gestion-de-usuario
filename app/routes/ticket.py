from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from app.database import db
from app.models.ticket import Ticket

ticket_bp = Blueprint("ticket", __name__, url_prefix="/tickets")


@ticket_bp.route("/")
def list_tickets():
    tickets = Ticket.query.order_by(Ticket.fecha_creacion.desc()).all()
    return render_template("ticket.html", tickets=tickets)


@ticket_bp.route("/create", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        fecha_creacion = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")

        fuentes = request.form.getlist("fuente_ticket")

        ticket = Ticket(
            titulo=request.form["titulo"],
            descripcion=request.form["descripcion"],
            fecha_creacion=fecha_creacion,
            estado=request.form["estado"],
            prioridad=request.form["prioridad"],
            nombre_cliente=request.form["nombre_cliente"],
            telefono_cliente=request.form["telefono_cliente"],
            correo_cliente=request.form["correo_cliente"],
            tipo_problema=request.form["tipo_problema"],
            fuente_ticket=", ".join(fuentes),
        )

        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for("ticket.list_tickets"))

    return render_template("ticket_form.html", ticket=None)


@ticket_bp.route("/<int:ticket_id>/edit", methods=["GET", "POST"])
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if request.method == "POST":
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        ticket.fecha_creacion = datetime.strptime(
            f"{fecha} {hora}", "%Y-%m-%d %H:%M"
        )

        ticket.titulo = request.form["titulo"]
        ticket.descripcion = request.form["descripcion"]
        ticket.estado = request.form["estado"]
        ticket.prioridad = request.form["prioridad"]
        ticket.nombre_cliente = request.form["nombre_cliente"]
        ticket.telefono_cliente = request.form["telefono_cliente"]
        ticket.correo_cliente = request.form["correo_cliente"]
        ticket.tipo_problema = request.form["tipo_problema"]
        ticket.fuente_ticket = ", ".join(request.form.getlist("fuente_ticket"))

        db.session.commit()
        return redirect(url_for("ticket.list_tickets"))

    return render_template("ticket_form.html", ticket=ticket)
