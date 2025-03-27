from pandas import DataFrame
from datetime import datetime


def extraer_valor(valor):
    return float(valor.replace(".", "").replace(",", "."))


def extraer_informacion_declaraciones():
    file_path = "FORMAS 99030.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        lineas = file.readlines()

    informacion = {}
    i = 0
    pag = 0
    for linea in lineas:
        informacion[i] = linea.strip()
        i += 1
    periodo = ""
    informacion_fiscal = {}
    dict_periodos = {}
    for num_linea, valores in informacion.items():
        contenido = valores.split()
        if (len(contenido) == 2 and "Página" not in contenido) or (
            "FORMA" in contenido and "99030" in contenido
        ):
            if contenido[0].isnumeric() and contenido[1].isnumeric():
                periodo = contenido[1] + contenido[0]
            if contenido[0] == "FORMA":
                per_planilla = periodo + "-" + contenido[4]
                informacion_fiscal[per_planilla] = dict_periodos

        elif "Página" in contenido:
            pag = contenido[1]

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
        elif "Excedente" in contenido and "Fiscales" in contenido and "20" in contenido:
            exced_cf_mes_anterior = {
                "Exced_cf_m_Ante": extraer_valor(contenido[14]),
            }
            dict_periodos.update(exced_cf_mes_anterior)

        elif "Excedente" in contenido and "Fiscal" in contenido and "60" in contenido:
            exced_cf_mes_siguiente = {
                "Exced_cf_m_Sig": extraer_valor(contenido[10]),
            }
            dict_periodos.update(exced_cf_mes_siguiente)

        elif (
            "Retenciones" in contenido
            and "Acumuladas" in contenido
            and "54" in contenido
        ):
            ret_acum = {
                "Ret_Acum": extraer_valor(contenido[6]),
            }
            dict_periodos.update(ret_acum)

        elif (
            "Retenciones" in contenido
            and "Descontadas" in contenido
            and "55" in contenido
        ):
            ret_descontadas = {
                "Ret_Desc": extraer_valor(contenido[9]),
            }
            dict_periodos.update(ret_descontadas)

        elif (
            "Retenciones" in contenido and "Período" in contenido and "66" in contenido
        ):
            ret_periodo = {
                "Ret_Periodo": extraer_valor(contenido[5]),
            }
            dict_periodos.update(ret_periodo)

        elif "SI" in contenido and "DECLARACIÓN" in contenido and "FECHA" in contenido:
            if pag == "1":
                dict_periodos.update(
                    {"Fecha": datetime.strptime(contenido[11], "%d/%m/%Y")}
                )

        elif "Total" in contenido and "Pagar" in contenido and "90" in contenido:
            dict_periodos.update({"Periodo": periodo})
            dict_periodos = {}

    # convertir a dataframe
    return DataFrame(informacion_fiscal).T  # Transponer


if __name__ == "__main__":
    datos = extraer_informacion_declaraciones()[
        [
            "Periodo",
            "Fecha",
            "Ventas Base Imponible",
            "Ventas No Gravadas",
            "Débito Fiscal",
            "Compras Base Imponible",
            "Compras No Gravadas",
            "Crédito Fiscal",
            "Exced_cf_m_Ante",
            "Exced_cf_m_Sig",
            "Ret_Acum",
            "Ret_Desc",
            "Ret_Periodo",
        ]
    ]
    datos.to_excel("informacion_fiscal.xlsx")
