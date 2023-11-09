# Configuración del proyecto

## 1. Crear + Activar [entorno virtual]

0. Descargar última versión de python.
1. Instalar phyton:

   - Hacer clic en el checkbox "Crear .path"
   - Btn Customize -> Hacer clic en el checkbox en el checkbox "Instalar en todos los usuarios"

2. Crear carpeta donde se va a trabajar
   - Crear carpeta raiz
   - Dentro de la carpeta crear entorno de virtual:
     cmd -> "python -m venv [nombre]\_env"
3. Activar el entorno virtual creado:
   cmd -> "cd .\nenv\Scripts\"
   cmd -> ".\activate"

   - Si tienes el error: "cannot be loaded because running scripts is disabled on this system"
     powershell(admin) -> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
     powershell(admin) -> Tipear "A" (acepta todo)
     Se activa el entorno virtual y verás que el path del cmd cambia en el inicio "([nombre]\_env)"

4. [opcional] Desactivar el entorno virtual:
   cmd -> "cd .\nenv\Scripts\"
   cmd -> "deactivate"

## 2. fastAPI - Ejecutar

1. En la barra lateral de vscode:

   - Click a "run & debug"
   - Ejecutar "Python: Current File"

2. Ingresar al navegador mediante:
   - http://127.0.0.1:8000/
   - http://127.0.0.1:8000/docs

## 3. Git

1. Para guardar las librerias / dependencias utilizadas en el proyecto:

   - pip freeze > requirements.txt

2. Para instalar las dependencias de un proyecto;
   - pip install -r requirements.txt

## Anexos

[1]

- Tutorial: "Entornos virtuales y paquetes"
  https://docs.python.org/es/3/tutorial/venv.html

- PowerShell bug “execution of scripts is disabled on this system.”
  https://stackoverflow.com/questions/54776324/powershell-bug-execution-of-scripts-is-disabled-on-this-system

[2]

- Debugging (fastAPI)
  https://fastapi.tiangolo.com/tutorial/debugging/

[3]

- pip freeze
  https://pip.pypa.io/en/stable/cli/pip_freeze/
