import re


def leer_file(archivo):
    with open(archivo, "r", encoding="utf-8") as file:
        lineas = file.readlines()

    informacion = {}
    i = 0
    for linea in lineas:
        informacion[i] = linea.strip()
        i += 1

    return informacion


def extraer_valor(valor):
    return float(valor.replace(".", "").replace(",", "."))


def extraer_informacion_fiscal(contenido_linea):
    valores = contenido_linea.split()
    resultado = {}

    if False:
        resultado = {
            "anio": valores[1],
            "mes": valores[0],
        }
    elif "Ventas" in valores and "no" in valores:
        resultado = {
            "Ventas No Gravadas": extraer_valor(valores[6]),
        }
    elif "Ventas" in valores and "Gravadas" in valores and "42" in valores:
        resultado = {
            "Ventas Base Imponible": extraer_valor(valores[8]),
            "Débito Fiscal": extraer_valor(valores[10]),
        }
    elif "Fiscal" in valores and "30" in valores:
        resultado = {
            "Compras No Gravadas": extraer_valor(valores[2]),
        }
    elif "Compras" in valores and "Gravadas" in valores and "33" in valores:
        resultado = {
            "Compras Base Imponible": extraer_valor(valores[8]),
            "Crédito Fiscal": extraer_valor(valores[10]),
        }

    return resultado


def main():
    archivo = "FORMA 99030 IVA DECLARACION 062024.txt"
    lee_archivo = leer_file(archivo)

    informacion_fiscal = {}
    for num_linea, contenido in lee_archivo.items():
        if contenido != "No existe":
            datos_fiscales = extraer_informacion_fiscal(contenido)
            if datos_fiscales:
                informacion_fiscal[num_linea] = datos_fiscales

    print(informacion_fiscal)


if __name__ == "__main__":
    main()
