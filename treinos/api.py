from typing import List

from ninja import Router
from .models import AlunosModel, AulasConcluidas
from .schemas import AlunoUpdateSchema, AlunosSchema, AlunosSchemaOut, Error, ProgressoAlunoSchema, AulaRealizadaSchema
from .graduacao import *
from datetime import date

treinos_router = Router()

@treinos_router.post('/aluno', response={200: AlunosSchemaOut, 400: Error})
def criar_um_aluno(request, aluno_schema:AlunosSchema):
    try:
        nome = aluno_schema.dict()['nome']
        email = aluno_schema.dict()['email']
        faixa = aluno_schema.dict()['faixa']
        data_nascimento = aluno_schema.dict()['data_nascimento']
        
        if AlunosModel.objects.filter(email=email).exists():
            return 400, {"message": 'Email já cadastrado'}

        aluno_criado = AlunosModel(
            nome=nome,
            email=email,
            faixa=faixa,
            data_nascimento=data_nascimento
        )
        aluno_criado.save()
        return AlunosSchemaOut(
            id=aluno_criado.id,
            nome=aluno_criado.nome,
            email=aluno_criado.email,
            faixa=aluno_criado.faixa,
            data_nascimento=aluno_criado.data_nascimento_formatada(),
        )
    except AlunosModel.DoesNotExist:
        return 400, {"message": 'Aluno não encontrado'}

@treinos_router.put('/aluno/{aluno_id}', response={200: AlunosSchemaOut, 400: Error})
def atualizar_um_aluno(request, aluno_schema:AlunoUpdateSchema, aluno_id: str):
    try:
        aluno = AlunosModel.objects.get(id=aluno_id)
        idade_aluno = date.today() - aluno.data_nascimento
        if int(idade_aluno.days / 365) < 18 and aluno_schema.dict()['faixa'] in ('A', 'R', 'M', 'P'):
            return 400, {"message": 'Aluno menor de 18 anos'}

        for attr, value in aluno_schema.dict().items():
            if value:
                setattr(aluno, attr, value)
        aluno.save()

        return AlunosSchemaOut(
            id=aluno_id,
            nome=aluno.nome,
            email=aluno.email,
            faixa=aluno.faixa,
            data_nascimento=aluno.data_nascimento_formatada(),
        )
    except AlunosModel.DoesNotExist:
        return 400, {"message": 'Aluno não encontrado'}

@treinos_router.get('/aluno', response={200: List[AlunosSchema], 400: Error})
def listar_todos_alunos(request):
    todos_alunos = AlunosModel.objects.all()
    if not todos_alunos:
        return 400, {"message": 'Algo saiu errado na busca de alunos'}
    return todos_alunos

@treinos_router.delete('/aluno/{aluno_id}', response={200: str, 400: Error})
def deletar_um_aluno(request, aluno_id: str):
    try:
        aluno = AlunosModel.objects.get(id=aluno_id)
        aluno.delete()
        return 200, 'Aluno deletado com sucesso'
    except AlunosModel.DoesNotExist:
        return 400, {"message": 'Aluno não encontrado'}

@treinos_router.get('/progresso-aluno', response={200: ProgressoAlunoSchema, 400: Error})
def progresso_do_aluno(request, email_aluno: str):
    aluno = AlunosModel.objects.get(email=email_aluno)
    total_aulas_concluidas = AulasConcluidas.objects.filter(aluno=aluno).count()
    faixa_atual = aluno.get_faixa_display()

    n = order_belt.get(faixa_atual, 0)
    total_aulas_proxima_faixa = calcula_aulas_necessarios_proximo_nivel(n)
    total_aulas_concluidas_faixa = AulasConcluidas.objects.filter(aluno=aluno, faixa_atual=aluno.faixa).count()
    aulas_necessarias = max(total_aulas_proxima_faixa - total_aulas_concluidas_faixa, 0)

    return ProgressoAlunoSchema(
        email=aluno.email,
        nome=aluno.nome,
        faixa=aluno.faixa,
        total_aulas=total_aulas_concluidas,
        aulas_necessarias_para_proxima_faixa=aulas_necessarias
    )

@treinos_router.post('/aula', response={200: str, 400: Error})
def registrar_uma_aula(request, aula_schema: AulaRealizadaSchema):
    qtd = aula_schema.dict()['qtd']
    email_aluno = aula_schema.dict()['email_aluno']

    if qtd <= 0:
        raise HttpError(400, 'Quantidade de aulas deve ser maior que zero')

    try:
        aluno = AlunosModel.objects.get(email=email_aluno)

        for _ in range(0, qtd):
            aulas_concluidas = AulasConcluidas(
                aluno=aluno,
                faixa_atual=aluno.faixa,
            )
            aulas_concluidas.save()
        
        return 200, f"Aula registrada com sucesso para o(a) {aluno.nome} ({aluno.email})"
    except AlunosModel.DoesNotExist:
        return 400, {"message": 'Aluno não encontrado'}
    
