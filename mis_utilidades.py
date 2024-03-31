
import glob


def read_credentials_from_file(config_file):
        try:
            with open(config_file, 'r') as file:
                lines = file.readlines()
                username = None
                password = None
               

                for line in lines:
                    if line.startswith("usuario:"):
                        username = line.split(":")[1].strip()
                        
                    elif line.startswith("clave:"):
                        password = line.split(":")[1].strip()
                        

                if username and password:
                    return username, password
                else:
                    print("Credenciales incompletas en el archivo de configuración. Debes ingresar las credenciales.")
                    username = input("Ingrese el usuario: ")
                    password = input("Ingrese la contraseña: ")
                    with open(config_file, 'w') as file:
                        file.write(f"usuario: {username}\nclave: {password}\n")
                    return username, password

        except FileNotFoundError:
            print("Archivo de configuración no encontrado. Debes ingresar las credenciales.")
            username = input("Ingrese el usuario: ")
            password = input("Ingrese la contraseña: ")
            with open(config_file, 'w') as file:
                file.write(f"usuario: {username}\nclave: {password}\n")
            return username, password


def obtener_archivo_con_indice_mas_alto(pattern):
    #hay que poner en importacion arriba del todo import glob
    archivos = glob.glob(pattern)
    numeros = [int(archivo.split('_')[-1].split('.')[0]) for archivo in archivos]
    if numeros:
        numero_mas_alto = max(numeros)
        return f'{pattern.split("*")[0]}{numero_mas_alto}.png'
    else:
        return ''