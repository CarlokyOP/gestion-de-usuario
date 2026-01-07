from flask import Blueprint, render_template, request, redirect, url_for
from app.database import db
from app.models.ticket import Ticket
from datetime import datetime

ticket_bp = Blueprint("ticket", __name__, url_prefix="/tickets")


@ticket_bp.route("/")
def list_tickets():
    tickets = Ticket.query.order_by(Ticket.fecha_creacion.desc()).all()
    return render_template("ticket.html", tickets=tickets)


@ticket_bp.route("/new", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":

        fecha = request.form.get("fecha")
        hora = request.form.get("hora")

        if fecha and hora:
            fecha_creacion = datetime.strptime(
                f"{fecha} {hora}", "%Y-%m-%d %H:%M"
            )
        else:
            fecha_creacion = datetime.utcnow()

        ticket = Ticket(
            titulo=request.form.get("titulo"),
            descripcion=request.form.get("descripcion"),
            fecha_creacion=fecha_creacion,
            estado=request.form.get("estado"),
            prioridad=request.form.get("prioridad"),
            nombre_cliente=request.form.get("nombre_cliente"),
            telefono_cliente=request.form.get("telefono_cliente"),
            correo_cliente=request.form.get("correo_cliente"),
            tipo_problema=request.form.get("tipo_problema"),
            fuente_ticket=request.form.get("fuente_ticket", "Llamada"),
        )

        db.session.add(ticket)
        db.session.commit()

        return redirect(url_for("ticket.list_tickets"))

    return render_template("ticket_form.html")


@ticket_bp.route("/<int:ticket_id>")
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template("ticket_detail.html", ticket=ticket)


@ticket_bp.route("/<int:ticket_id>/edit", methods=["GET", "POST"])
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if request.method == "POST":

        fecha = request.form.get("fecha")
        hora = request.form.get("hora")

        if fecha and hora:
            ticket.fecha_creacion = datetime.strptime(
                f"{fecha} {hora}", "%Y-%m-%d %H:%M"
            )

        ticket.titulo = request.form.get("titulo")
        ticket.descripcion = request.form.get("descripcion")
        ticket.estado = request.form.get("estado")
        ticket.prioridad = request.form.get("prioridad")
        ticket.nombre_cliente = request.form.get("nombre_cliente")
        ticket.telefono_cliente = request.form.get("telefono_cliente")
        ticket.correo_cliente = request.form.get("correo_cliente")
        ticket.tipo_problema = request.form.get("tipo_problema")
        ticket.fuente_ticket = request.form.get("fuente_ticket")

        db.session.commit()
        return redirect(url_for("ticket.list_tickets"))

    return render_template("ticket_form.html", ticket=ticket)


@ticket_bp.route("/<int:ticket_id>/delete", methods=["POST"])
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    return redirect(url_for("ticket.list_tickets"))
