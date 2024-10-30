# Importamos las bibliotecas necesarias
from nicegui import ui
import numpy as np

# Función para calcular la transpuesta de la matriz
def calcular_transpuesta(matriz):
    return matriz.T

# Función principal de la aplicación
@ui.page('/')
def main():
    with ui.column():
        ui.label("Calculadora de operaciones matriciales")

        # Selección de la operación a realizar (solo Transpuesta en este caso)
        # if operacion == 'Transpuesta':
        #     resultado = calcular_transpuesta(matriz)
        # elif operacion == 'Determinante':
        #     if matriz.shape[0] != matriz.shape[1]:
        #         ui.notify('El determinante solo se puede calcular en matrices cuadradas.', color='red')
        #         return
        #     resultado_valor = calcular_determinante(matriz)
        #     resultado = f"El determinante de la matriz es: {resultado_valor:.2f}"
        # elif operacion == 'Inversa':
        #     if matriz.shape[0] != matriz.shape[1]:
        #         ui.notify('La inversa solo se puede calcular en matrices cuadradas.', color='red')
        #         return
        #     resultado = calcular_inversa(matriz)
        # elif operacion == 'Rango':
        #     rango = calcular_rango(matriz)
        #     resultado = f"El rango de la matriz es: {rango}"
        # elif operacion == 'Eliminación Gaussiana':
        #     resultado = eliminacion_gaussiana(matriz)
        # else:
        #     ui.notify('Operación no soportada.', color='red')
        #     return
        operaciones = ['Transpuesta']  # Puedes agregar más operaciones aquí
        operacion_seleccionada = ui.select(operaciones, label='Seleccione la operación', value='Transpuesta')

        # Entrada para el número de filas y columnas
        filas = ui.number(label="Número de filas", value=2, min=1)
        columnas = ui.number(label="Número de columnas", value=2, min=1)

        matriz_inputs = []

        # Botón para generar la matriz
        def generar_matriz():
            # Limpia cualquier campo de entrada anterior
            for row in matriz_inputs:
                for cell in row:
                    cell.delete()
            matriz_inputs.clear()

            # Crear campos de entrada para la matriz según el tamaño especificado
            for i in range(int(filas.value)):
                row = []
                with ui.row():
                    for j in range(int(columnas.value)):
                        input_cell = ui.number(label=f"Elemento ({i+1},{j+1})", value=0)
                        row.append(input_cell)
                matriz_inputs.append(row)

        ui.button("Generar Matriz", on_click=generar_matriz)

        # Botón para resolver la matriz y mostrar el resultado
        def on_resolver_click():
            if not matriz_inputs:
                ui.notify('Por favor, genere la matriz primero.', color='red')
                return
            try:
                # Crear la matriz a partir de los valores ingresados
                matriz = np.array([[float(cell.value) for cell in row] for row in matriz_inputs])

                # Realizar la operación seleccionada
                resultado = None
                operacion = operacion_seleccionada.value

                if operacion == 'Transpuesta':
                    resultado = calcular_transpuesta(matriz)
                else:
                    ui.notify('Operación no soportada.', color='red')
                    return

                # Mostrar el resultado
                ui.label("Resultado:").classes('mt-5')
                if isinstance(resultado, np.ndarray):
                    mostrar_matriz(resultado)
                else:
                    # Mostrar resultados escalares
                    ui.label(str(resultado))

            except Exception as e:
                ui.notify(f'Error inesperado: {e}', color='red')

        ui.button("Resolver", on_click=on_resolver_click).classes('mt-5')

        # Función para mostrar la matriz en una tabla
        def mostrar_matriz(matriz):
            # Convertir la matriz NumPy en una lista de diccionarios
            data = []
            for idx_row, row in enumerate(matriz):
                row_dict = {'fila': idx_row + 1}
                for idx_col, cell in enumerate(row):
                    row_dict[f'col_{idx_col+1}'] = f"{cell}"
                data.append(row_dict)

            # Definir las columnas de la tabla
            columnas = [{'name': 'fila', 'label': '', 'field': 'fila'}]
            for idx_col in range(matriz.shape[1]):
                columnas.append({'name': f'col_{idx_col+1}', 'label': f'Col {idx_col+1}', 'field': f'col_{idx_col+1}'})

            # Crear la tabla con los datos y columnas definidos
            ui.table(columns=columnas, rows=data).classes('mt-5')

        # Tip:
        # - Puedes agregar más operaciones a la lista 'operaciones', como 'Determinante', 'Inversa', etc.
        # - Luego, implementa las funciones correspondientes y amplía el bloque if-elif en 'on_resolver_click'.
        # - Asegúrate de manejar casos especiales, como matrices no cuadradas para el determinante y la inversa.
        # - Añade validaciones y mensajes de error para mejorar la experiencia del usuario.

ui.run()
