#Importar el framework de fastapi
from fastapi import FastAPI, HTTPException, status, APIRouter
#Crear objeto a partir de la clase FastAPI
app = FastAPI()
#Importar la carperta router
from routers import router1 #el nombre del router



#importar pydantic para obtener una entidad que pueda definir usuarios
from pydantic import BaseModel, ValidationError

#importar pandas 
import pandas as pd
#Importar la librería para manejar archivos
import os   

app.include_router(router1.router)

#---------------------------------------------------------------------
 
 #Actividad 5: API con CRUD
 #Actividad 6: Respuesta HTTP
 #Actividad 7: Routers 
  
#Definir la clase Alumno para el modelo de datos
class Alumno(BaseModel):
    Matricula: int
    Nombre: str
    Edad: int
    Facultad: str
    Grado: str
    Carrera: str
    Genero: str
    Correo: str
    Promedio: float
    Semestre: int

#Copiar los datos del csv de los alumnos y convertirlo en una lista compatible con el modelo Alumno
def cargar_datos_alumnos():
    df =pd.read_csv('BD_E6_v2.csv')
    lista_alumnos = df.to_dict(orient='records')
    return lista_alumnos

#Lista para almacenar los alumnos
alumnos = cargar_datos_alumnos()

# 1. Consultar todos los alumnos
@app.get("/alumnos/", status_code=status.HTTP_200_OK)
def get_alumnos():
    return alumnos

# 2. Consultar un alumno por matrícula
@app.put("/alumnos/", status_code=status.HTTP_200_OK)
async def consulta_alumno(alumno: Alumno):
    #Verificar si el alumno existe
    found = False
    for saved_user in alumnos:
        if saved_user["Matricula"] == alumno.Matricula:
            found = True
            return saved_user
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha encontrado el alumno")

# 3. Agregar un nuevo alumno
@app.post("/alumnos/", status_code=status.HTTP_201_CREATED)
async def nuevo_alumno(alumno: Alumno):
    # Verificar si el alumno ya existe por matrícula
    for saved_user in alumnos:
        if saved_user["Matricula"] == alumno.Matricula:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El alumno ya existe")
    # Si no existe, agregarlo
    alumnos.append(alumno.model_dump())
    return alumno

# 4. Modificar un alumno existente
@app.put("/alumnos/", status_code=status.HTTP_200_OK)
async def modificar_alumno(alumno: Alumno):
    found = False #Bandera para verificar si se encontró el alumno
    
    for index, saved_user in enumerate(alumnos):
        if saved_user["Matricula"] == alumno.Matricula:
            alumnos[index] = alumno.model_dump()
            found = True
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha actualizado el alumno")
    return alumno

# 5. Eliminar un alumno
@app.delete("/alumnos/", status_code=status.HTTP_200_OK)
async def eliminar_alumno(alumno: Alumno):
    # Verificar si el alumno existe
    found = False
    for index, saved_user in enumerate(alumnos):
        if saved_user["Matricula"] == alumno.Matricula:
            del alumnos[index]
            found = True
            return {"message": "Alumno eliminado"}
            break
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha eliminado el alumno")
    


#------------------Lista de responses ------------------------------- 
# 200: OK // todo bien con la consulta
# 201: Created // se creo correctamente el alumno
# 409: Conflict // el alumno ya existe
# 404: Not Found // no se encontro el alumno
# 422: Unprocessable Entity // error de validación de datos, por ejemplo, un campo requerido no se proporcionó o un campo tiene un tipo de dato incorrecto