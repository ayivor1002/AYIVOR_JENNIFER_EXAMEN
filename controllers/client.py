
def pdf(pdf_nom: str, place: object):
    def f(d:str):
        if d[0] == "0":
            return d[1]
        return d
    from fpdf import FPDF
    import os
    import datetime
    pdf = FPDF()
    pdf.add_page()

    #pdf.set_font("Arial", size=15)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10,txt="Nom et Prénom : "+place.personne_id.nom +" "+place.personne_id.prenom, ln=1, align="C")

    pdf.cell(50, 12,txt="Film à suivre : "+place.affiche_id.film_id.titre, ln=1,align="L")
    
    pdf.cell(50, 13,txt="Durée du Film : "+place.affiche_id.film_id.duree, ln=1,align="L")
    pdf.cell(50, 14,txt="Date de sortie du Film : "+place.affiche_id.film_id.date_sortie.__str__(), ln=1,align="L")
    pdf.cell(50, 15,txt="Réalisateur du Film : "+place.affiche_id.film_id.realisateur, ln=1,align="L")
    pdf.cell(50, 16,txt="Nombre de place que vous avez réservés pour ce Film : "+str(place.nombre_place), ln=1,align="L")

    jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    mois_annee = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    dateComplet = str(place.affiche_id.date_heure_projection.__str__().split(" ")[0])
    heures = str(place.affiche_id.date_heure_projection.__str__().split(" ")[1])
    dateComplet = dateComplet.split("-")
    w = datetime.date(int(dateComplet[0]), int(f(dateComplet[1])), int(f(dateComplet[2]))).isocalendar()
    pdf.cell(200, 20,txt=jours_semaine[w[2] - 1] + ", le "+f(dateComplet[2]) + " " + mois_annee[int(f(dateComplet[1])) - 1] + " " + dateComplet[0] + ", "+heures, ln=1, align="R")

    ''' 
    .cell(w, h = 0, txt = '', border = 0, ln = 0, 
          align = '', fill = False, link = '')
     '''


    file_url = "./applications/gestion_cinema_web2py/static/"+ pdf_nom
    pdf.output(file_url)

def open_pdf(pdf_nom: str):
    import webbrowser
    path = 'http://127.0.0.1:8000/gestion_cinema_web2py/static/'+ pdf_nom
    webbrowser.open_new(path)
def open_pdf_url(url_pdf: str):
    import webbrowser
    path = url_pdf
    webbrowser.open_new(path)


@auth.requires_login()
def ajout_client():
    form = SQLFORM(db.clients)
    if form.process().accepted:
        session.flash = "Le client a été ajouté avec succès !"
        redirect(URL('liste_clients'))
    return response.render('client/ajout.html', dict(form=form))
  
    


@auth.requires_login()
def liste_clients():
    rows = db().select(db.clients.ALL)
    return dict(rows=rows )



@auth.requires_login()
def supprimer_client():
    db(db.clients.id ==  request.args(0)).delete()
        
    return dict(form=redirect(URL('liste_clients')), message=T('Un enrégistrement d\'un client a été supprimé'))

@auth.requires_login()
def modifier_client():
    client = db.clients(request.args(0)) or redirect(URL('error'))
    form = SQLFORM(db.clients, client)
    form.process(detect_record_change=True)
    if form.record_changed:
        response.flash = 'form changed'
        return dict(form=redirect(URL('liste_clients')))
    elif form.accepted:
        response.flash = 'form accepted'
        return dict(form=redirect(URL('liste_clients')))
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

    