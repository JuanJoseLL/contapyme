

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi(' Lina Lopez, ¿Lista para trabajar?')

import pandas as pd

pd.set_option('display.max_rows', None)


def read_file(file):
    # Cargar el archivo Excel en un DataFrame de Pandas
    try:
        dataframe = pd.read_excel(file, engine='openpyxl')
        return dataframe
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return None


def read_banc(file):
    try:
        # Leer el archivo Excel
        df = pd.read_excel(file, engine='openpyxl')

        # Filtrar las filas que no contienen los valores específicos en 'DESCRIPCION'
        df_filtrado = df[~df['DESCRIPCION'].isin(
            ['COMISION PAGO DE NOMINA', 'COBRO IVA PAGOS AUTOMATICOS', 'RTE FUENTE MASTER', 'RTE ICA MASTER',
             'RTE ICA VISA', 'RTE FUENTE VISA', 'COMISION BOTON', 'IVA BOTON', 'IMPTO GOBIERNO 4X1000',
             'COBRO IVA PAGOS AUTOMATICOS', 'COMISION MASTER', 'COMISION PAGO A OTROS BANCOS',
             'COMISION PAGO A PROVEEDORES', 'COMISION PSE', 'COMISION VISA', 'IVA COMISION PSE',
             'AJUSTE INTERESES SOBREG N DIAS', 'CUOTA MANEJO SUC VIRT EMPRESA', 'INTERESES DE SOBREGIRO',
             'IVA CUOTA MANEJO SUC VIRT EMP'])]

        return df_filtrado
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None


# Prueba la función con un archivo Excel
banc_file = 'BANCOLOMBIA.xlsx'
conta_file = 'CONTAPYME.xlsx'
bancolombia = read_banc(banc_file)
conta_pymes = read_file(conta_file)


def to_number(df, columna):
    # Eliminar separadores de miles (puntos) y cambiar comas por puntos para decimales
    #print(df)
    df[columna] = df[columna].str.replace('.', '', regex=False)
    #print(df)
    # Convertir la columna a numérico, usando 'coerce' para manejar valores no válidos
    df[columna] = pd.to_numeric(df[columna], errors='coerce')


def find_missing_values(df1, col1, df2, col2):
    # Convertir los valores de las columnas a conjuntos de strings
    set_df1 = set(df1[col1].astype(str))
    set_df2 = set(df2[col2].astype(str))

    # Encontrar valores que están en df1 pero no en df2

    missing_values = set_df1.difference(set_df2)

    # Filtrar el DataFrame df1 para obtener solo las filas con los valores faltantes
    faltantes = df1[df1[col1].astype(str).isin(missing_values)]

    return faltantes


def find_missing_values_num(df1, col1, df2, col2):
    # Filtrar NaNs antes de convertir a conjuntos
    set_df1 = set(df1[~df1[col1].isna()][col1])
    set_df2 = set(df2[~df2[col2].isna()][col2])

    # Encontrar valores que están en df1 pero no en df2
    missing_values = set()
    for value in set_df1:
        if not any(abs(value - other_value) <= 1 for other_value in set_df2):
            missing_values.add(value)

    # Filtrar el DataFrame df1 para obtener solo las filas con los valores faltantes
    faltantes = df1[df1[col1].apply(lambda x: x in missing_values)]

    return faltantes


bancolombia['VALOR'] = bancolombia['VALOR'].str[:-3]
to_number(bancolombia, 'VALOR')
to_number(conta_pymes, 'Total')

# bancolombia['VALOR'] = bancolombia['VALOR'].astype(str)
# conta_pymes['Total'] = conta_pymes['Total'].astype(str)

#print(bancolombia)
#print(conta_pymes)

faltantes = find_missing_values_num(bancolombia, 'VALOR', conta_pymes, 'Total')
filas_encontradas = conta_pymes[conta_pymes['Total'] == -2742765]
banc = bancolombia[bancolombia['VALOR'] == -2742764]

#print(filas_encontradas)
#print(banc)

faltantes.to_excel("faltantes.xlsx", index=False)
#print(faltantes)
#print(faltantes.shape[0])
