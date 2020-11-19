from pymongo import database
from datetime import datetime

def adicionar_user(db: database, member):
    data = {
        "_id": member.id,
        "nome_real": None,
        "nome": member.name,
        "discriminador": member.discriminator,
        "avatar": member.avatar,
        "administrador": False,
        "moderador": False,
        "helper": False,
        "mutado": False,
        "reps": 0,
        "reps_totais": 0,
        "lembrete_votar": False,
        "lembrete_enviado": False,
        "próximo_voto": None,
        "próximo_rep": None,
        "linguagem":None,
        "linguagem2":None,
        "aceito_por":None,
        "descoberto_em": datetime.now(),
        "banido": False,
        "ban_info": {
            "autor": None,
            "motivo": None,
            "data": None
        },
        "histórico_nomes": [
            {
                "nome": str(member),
                "data": datetime.utcnow()
            }
        ],
        "histórico_reps": [],
        "histórico_votos": []
    }

    return db.insert_one(data)