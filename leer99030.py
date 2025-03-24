import re
from pandas import DataFrame


def extraer_valor(valor):
    return float(valor.replace(".", "").replace(",", "."))


def extraer_informacion_declaraciones():
    file_path = "FORMAS 99030.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        lineas = file.readlines()

    informacion = {}
    i = 0
    for linea in lineas:
        informacion[i] = linea.strip()
        i += 1
    periodo = ""
    informacion_fiscal = {}
    dict_periodos = {}
    for num_linea, valores in informacion.items():
        contenido = valores.split()
        if len(contenido) == 2 or ("FORMA" in contenido and "99030" in contenido):
            if contenido[0].isnumeric() and contenido[1].isnumeric():
                periodo = contenido[1] + contenido[0]
            if contenido[0] == "FORMA":
                per_planilla = periodo + "-" + contenido[4]
                informacion_fiscal[per_planilla] = dict_periodos
                dict_periodos = {}
                dict_periodos.update({"Periodo": periodo})
        elif "Ventas" in contenido and "no" in contenido:

            ventas_no_gravadas = {
                "Ventas No Gravadas": extraer_valor(contenido[6]),
            }
            dict_periodos.update(ventas_no_gravadas)

        elif "Ventas" in contenido and "Gravadas" in contenido and "42" in contenido:
            ventas_gravadas = {
                "Ventas Base Imponible": extraer_valor(contenido[8]),
                "Débito Fiscal": extraer_valor(contenido[10]),
            }
            dict_periodos.update(ventas_gravadas)

        elif "Fiscal" in contenido and "30" in contenido:
            compras_no_gravadas = {
                "Compras No Gravadas": extraer_valor(contenido[2]),
            }
            dict_periodos.update(compras_no_gravadas)

        elif "Compras" in contenido and "Gravadas" in contenido and "33" in contenido:
            compras_gravadas = {
                "Compras Base Imponible": extraer_valor(contenido[8]),
                "Crédito Fiscal": extraer_valor(contenido[10]),
            }
            dict_periodos.update(compras_gravadas)

    # convertir a dataframe
    return DataFrame(informacion_fiscal).T  # Transponer


if __name__ == "__main__":
    datos = extraer_informacion_declaraciones()[
        [
            "Periodo",
            "Ventas Base Imponible",
            "Ventas No Gravadas",
            "Débito Fiscal",
            "Compras Base Imponible",
            "Compras No Gravadas",
            "Crédito Fiscal",
        ]
    ]
    datos.to_excel("informacion_fiscal.xlsx")
