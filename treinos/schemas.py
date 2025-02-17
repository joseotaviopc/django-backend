from typing import Optional
from ninja import ModelSchema, Schema
from .models import AlunosModel

class AlunosSchema(ModelSchema):
    class Meta:
        model = AlunosModel
        fields = ['id', 'nome', 'email', 'faixa', 'data_nascimento']

class AlunoUpdateSchema(Schema):
    nome: str = None
    email: str = None
    faixa: str = None
    data_nascimento: str = None

class AlunosSchemaOut(Schema):
    id: str
    nome: str
    email: str
    faixa: str
    data_nascimento: str

class ProgressoAlunoSchema(Schema):
    email: str
    nome: str
    faixa: str
    total_aulas: int
    aulas_necessarias_para_proxima_faixa: int

class AulaRealizadaSchema(Schema):
    qtd: Optional[int] = 1
    email_aluno: str

class Error(Schema):
    message: str