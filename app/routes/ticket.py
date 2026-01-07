@ticket_bp.route("/create", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":

        fecha_str = request.form.get("fecha")
        hora_str = request.form.get("hora")

        if fecha_str and hora_str:
            fecha_creacion = datetime.strptime(
                f"{fecha_str} {hora_str}", "%Y-%m-%d %H:%M"
            )
        else:
            fecha_creacion = datetime.utcnow()

        # Fuente del ticket
        fuentes = request.form.getlist("fuente_ticket")
        fuente_ticket = ", ".join(fuentes)

        # Tipo de problema (radio → uno solo)
        tipo_problema = request.form.get("tipo_problema")

        ticket = Ticket(
            titulo=request.form.get("titulo"),
            descripcion=request.form.get("descripcion"),
            fecha_creacion=fecha_creacion,
            estado=request.form.get("estado"),
            prioridad=request.form.get("prioridad"),

            nombre_cliente=request.form.get("nombre_cliente") or "No informado",
            telefono_cliente=request.form.get("telefono_cliente") or "No informado",
            correo_cliente=request.form.get("correo_cliente") or "No informado",

            tipo_problema=tipo_problema,
            fuente_ticket=fuente_ticket,

            medidas_adoptadas=request.form.get("medidas_adoptadas"),
            resolucion=request.form.get("resolucion"),
            tecnico_a_cargo=request.form.get("tecnico_a_cargo"),
        )

        db.session.add(ticket)
        db.session.commit()

        return redirect(url_for("ticket.list_tickets"))

    return render_template("ticket_form.html", ticket=None)

