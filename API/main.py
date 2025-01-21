import atexit, sqlite3
from fastapi import FastAPI
from models.CursoModel import Curso 

app = FastAPI()
conexao = sqlite3.connect("../reuso.db")
cursor = conexao.cursor()
    
def encerrarCursor():
    cursor.close()

@app.get("/cursos")
async def listarCursos():
    
    requisicao = f"""
        SELECT * FROM cursos;
    """
    try:
        cursor.execute(requisicao)
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        return {"error": e}
    

@app.post("/cursos")
async def criarCurso(curso: Curso):
    
    requisicao = f"""
            INSERT INTO cursos (title, description, ch) 
            VALUES (?, ?, ?);
        """
    
    try:
        cursor.execute(requisicao, (curso.title, curso.description, curso.ch))
        conexao.commit()
        return {"message": f"Curso '{curso.title}' adicionado com sucesso!"} 
    
    except Exception as e:
        return {"error": e}    

@app.get("/cursos/{id}")
async def detalhesCurso(id: int):
    
    requisicao = f"""
            SELECT * FROM cursos WHERE id = ?;
        """
    
    try:
        cursor.execute(requisicao, (id, ))
        resultado = cursor.fetchone()
        if resultado:
            return resultado
        else:
            return {"message": "Curso não encontrado."}
    
    except Exception as e:
        return {"error": e} 

@app.put("/cursos/{id}")
async def atualizarCurso(curso: Curso, id: int):

    requisicao = f"""
        UPDATE cursos
        SET title = ?, description = ?, ch = ?
        WHERE id = ?;
    """

    try:
        cursor.execute(requisicao, (curso.title, curso.description, curso.ch, id))
        conexao.commit()
        return {"message": f"Curso com id '{id}' alterado com sucesso!"} 
    
    except Exception as e:
        return {"error": e}  

@app.delete("/cursos/{id}")
async def excluirCurso(id: int):
    requisicao = f"""
        DELETE FROM cursos WHERE id = ?;
    """

    try:
        cursor.execute(requisicao, (id, ))
        conexao.commit()
        return {"message": f"Curso com id '{id}' excluído com sucesso!"} 
    
    except Exception as e:
        return {"error": e}  

atexit.register(encerrarCursor)