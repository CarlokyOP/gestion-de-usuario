from flask import Blueprint, render_template, request, redirect, url_for
from app.database import db
from app.models.ticket import Ticket
from datetime import datetime

ticket_bp = Blueprint("ticket", __name__, url_prefix="/tickets")

@ticket_bp.route("/")
def list_tickets():
    tickets = Ticket.query.order_by(Ticket.fecha_creacion.desc()).all()
    return render_template("ticket.html", tickets=tickets)


@ticket_bp.route("/create", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":
        fecha = request.form.get("fecha")
        hora = request.form.get("hora")
        fecha_creacion = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")

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
            fuente_ticket=request.form["fuente_ticket"],
        )

        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for("ticket.list_tickets"))

    return render_template("ticket_form.html")
