from pandas import DataFrame
from datetime import datetime


def extraer_valor(valor):
    return float(valor.replace(".", "").replace(",", "."))


def extraer_informacion_declaraciones():
    file_path = "FORMAS 99030.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        lineas = file.readlines()

    informacion_fiscal = {}
    dict_periodos = {}
    periodo = ""
    pag = 0

    def actualizar_dict_periodos(clave, valor):
        dict_periodos[clave] = extraer_valor(valor)

    for linea in lineas:
        contenido = linea.strip().split()

        if len(contenido) == 2 and "Página" not in contenido:
            if contenido[0].isnumeric() and contenido[1].isnumeric():
                periodo = contenido[1] + contenido[0]

        elif "FORMA" in contenido and "99030" in contenido:
            per_planilla = periodo + "-" + contenido[4]
            informacion_fiscal[per_planilla] = dict_periodos

        elif "Página" in contenido:
            pag = contenido[1]

        elif "Ventas" in contenido and "no" in contenido:
            actualizar_dict_periodos("Ventas No Gravadas", contenido[6])

        elif "Ventas" in contenido and "Gravadas" in contenido and "42" in contenido:
            actualizar_dict_periodos("Ventas Base Imponible", contenido[8])
            actualizar_dict_periodos("Débito Fiscal", contenido[10])

        elif "Fiscal" in contenido and "30" in contenido:
            actualizar_dict_periodos("Compras No Gravadas", contenido[2])

        elif "Compras" in contenido and "Gravadas" in contenido and "33" in contenido:
            actualizar_dict_periodos("Compras Base Imponible", contenido[8])
            actualizar_dict_periodos("Crédito Fiscal", contenido[10])

        elif "Excedente" in contenido and "Fiscales" in contenido and "20" in contenido:
            actualizar_dict_periodos("Exced_cf_m_Ante", contenido[14])

        elif "Excedente" in contenido and "Fiscal" in contenido and "60" in contenido:
            actualizar_dict_periodos("Exced_cf_m_Sig", contenido[10])

        elif (
            "Retenciones" in contenido
            and "Acumuladas" in contenido
            and "54" in contenido
        ):
            actualizar_dict_periodos("Ret_Acum", contenido[6])

        elif (
            "Retenciones" in contenido
            and "Descontadas" in contenido
            and "55" in contenido
        ):
            actualizar_dict_periodos("Ret_Desc", contenido[9])

        elif (
            "Retenciones" in contenido and "Período" in contenido and "66" in contenido
        ):
            if len(contenido) > 5:
                actualizar_dict_periodos("Ret_Periodo", contenido[5])

        elif (
            "SI" in contenido
            and "DECLARACIÓN" in contenido
            and "FECHA" in contenido
            and pag == "1"
        ):
            dict_periodos["Fecha"] = datetime.strptime(contenido[11], "%d/%m/%Y")

        elif "Total" in contenido and "Pagar" in contenido and "90" in contenido:
            dict_periodos["Periodo"] = periodo
            dict_periodos = {}

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
