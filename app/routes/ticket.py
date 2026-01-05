from flask import Blueprint, render_template, request, redirect, url_for
from app.models.ticket import Ticket
from app import db

ticket_bp = Blueprint('ticket', __name__)

# LISTADO
@ticket_bp.route('/')
def list_tickets():
    tickets = Ticket.query.all()
    return render_template('ticket.html', tickets=tickets)

# FORMULARIO NUEVO
@ticket_bp.route('/new')
def new_ticket():
    return render_template('ticket_form.html')

# CREAR TICKET
@ticket_bp.route('/create', methods=['POST'])
def create_ticket():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    prioridad = request.form['prioridad']

    ticket = Ticket(
        titulo=titulo,
        descripcion=descripcion,
        prioridad=prioridad,
        estado='Abierto'
    )

    db.session.add(ticket)
    db.session.commit()

    return redirect(url_for('ticket.list_tickets'))

# DETALLE
@ticket_bp.route('/<int:ticket_id>')
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template('ticket_detail.html', ticket=ticket)

# CAMBIAR ESTADO
@ticket_bp.route('/<int:ticket_id>/status/<estado>')
def change_status(ticket_id, estado):
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.estado = estado
    db.session.commit()
    return redirect(url_for('ticket.ticket_detail', ticket_id=ticket.id))
