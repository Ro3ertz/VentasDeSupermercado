# -*- coding: utf-8 -*-
"""
@author: roobe
"""
import pandas as pd

#Cragar el archivo
file_path = "C:/Users/roobe/Downloads/supermarket_sales - Sheet1.csv"
df = pd.read_csv(file_path)

#Primeras filas del dataset
df.head()

"""
 Estructura del Dataset
Contiene información sobre ventas en un supermercado, incluyendo:
Datos de facturación: Invoice ID, Date, Time
Ubicación: Branch, City
Cliente: Customer type, Gender
Detalles de compra: Product line, Unit price, Quantity, Tax 5%, Total
Pago: Payment
Rentabilidad: cogs (Costo de los bienes vendidos), gross income, gross margin percentage
Satisfacción: Rating
"""

#Verificar los tipos de datos y valores nulos
df.info()

#Verificar los valores nulos
missing_values = df.isnull().sum()
missing_values

"""
Observaciones del Análisis Inicial
El dataset contiene 1000 registros y 17 columnas.
No hay valores nulos.
Tipos de datos:
Variables numéricas: Unit price, Quantity, Tax 5%, Total, cogs, gross margin percentage, gross income, Rating.
Variables categóricas: Branch, City, Customer type, Gender, Product line, Payment.
Fechas y tiempos: Date (tipo object), Time (tipo object).
"""

#Convertir la columna 'Date' a formato de fecha
df['Date'] = pd.to_datetime(df['Date'])
#Convertir la columna 'Time' a formato de hora
df['Time'] = pd.to_datetime(df['Time'], format = '%H:%M').dt.time

#Obtener estadísticas descriptivas para las variables númericas
stats_num = df.describe()
#Obtener estadísticas descriptivas para las variables categoricas
stats_cat = df.describe(include=['object'])

#Resultados
print(stats_num)
print(stats_cat)

"""
Resumen del Análisis Estadístico

Variables Numéricas
La cantidad de productos por compra varía entre 1 y 10 unidades.
El precio unitario promedio es de aproximadamente 55.67.
La ganancia bruta (gross income) tiene una media de 15.38, con un margen constante de 4.76%.
El rating promedio de las compras es 6.97, con valores entre 4 y 10.

Variables Categóricas 
Hay tres sucursales (Branch): A (Yangon), B (Mandalay), C (Naypyitaw), con 340 transacciones cada una.
Los tipos de clientes (Customer type) están bien distribuidos entre "Member" (501) y "Normal" (499).
Los métodos de pago incluyen Ewallet (345 compras), Cash (344), Credit Card (311).
La categoría de producto más vendida es "Fashion Accessories" (178 compras).
Existen 506 horarios únicos de compra, con un pico a las 19:48
"""

import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de estilo
plt.style.use('ggplot')

# Gráfico de distribución de ventas por categoría de producto
plt.figure(figsize=(10, 6))
sns.countplot(y=df['Product line'], order=df['Product line'].value_counts().index, palette="viridis")
plt.title("Cantidad de Ventas por Categoría de Producto", fontsize=14)
plt.xlabel("Número de Ventas")
plt.ylabel("Categoría de Producto")
plt.show()

# Gráfico de métodos de pago más utilizados
plt.figure(figsize=(8, 5))
sns.countplot(x=df['Payment'], order=df['Payment'].value_counts().index, palette="muted")
plt.title("Métodos de Pago Más Usados", fontsize=14)
plt.xlabel("Método de Pago")
plt.ylabel("Cantidad de Compras")
plt.show()

# Gráfico de rating de clientes
plt.figure(figsize=(10, 5))
sns.histplot(df['Rating'], bins=20, kde=True, color="blue")
plt.title("Distribución de Ratings de Clientes", fontsize=14)
plt.xlabel("Rating")
plt.ylabel("Frecuencia")
plt.show()

"""
 Análisis de las Visualizaciones
Ventas por Categoría de Producto

La categoría más vendida es "Fashion Accessories", seguida de "Food and Beverages".
La menos vendida es "Health and Beauty", lo que puede indicar menor demanda en este sector.
Métodos de Pago Más Utilizados

Ewallet es el método de pago más popular, seguido de Cash y Credit Card.
Esto sugiere que los clientes prefieren métodos digitales sobre efectivo.
Distribución de Ratings de Clientes

La mayoría de los clientes califican su experiencia con valores entre 5 y 9.
Hay menos calificaciones bajas, lo que indica un servicio en general satisfactorio.
"""

# Convertir la columna 'Time' a horas para análisis por franja horaria
df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour

# Agrupar por hora del día y contar transacciones
sales_by_hour = df['Hour'].value_counts().sort_index()

# Gráfico de ventas por hora del día
plt.figure(figsize=(10, 5))
sns.lineplot(x=sales_by_hour.index, y=sales_by_hour.values, marker="o", color="red")
plt.title("Número de Compras por Hora del Día", fontsize=14)
plt.xlabel("Hora del Día")
plt.ylabel("Cantidad de Compras")
plt.xticks(range(7, 22))  # Tienda opera entre 7 AM y 9 PM
plt.grid(True)
plt.show()

"""
Análisis de Compras por Hora del Día
La tienda tiene un flujo de ventas constante durante el día.
El pico de compras ocurre entre las 12:00 y las 14:00 horas, posiblemente durante la hora de almuerzo.
Hay un segundo pico entre las 18:00 y 20:00 horas, indicando que muchas compras se realizan después del trabajo.
Las ventas son más bajas en la mañana (7:00 - 10:00 AM).
"""

# Agrupar por sucursal y calcular ventas totales
sales_by_branch = df.groupby("Branch")["Total"].sum().sort_values(ascending=False)

# Gráfico de ventas totales por sucursal
plt.figure(figsize=(8, 5))
sns.barplot(x=sales_by_branch.index, y=sales_by_branch.values, palette="pastel")
plt.title("Ventas Totales por Sucursal", fontsize=14)
plt.xlabel("Sucursal")
plt.ylabel("Ventas Totales ($)")
plt.show()

"""
Análisis de Ventas por Sucursal
Las tres sucursales tienen ventas similares, lo que indica una distribución equitativa del negocio.
La sucursal con mayores ventas es "A" (Yangon), seguida de "B" (Mandalay) y "C" (Naypyitaw).
Esto sugiere que Yangon tiene más demanda o un ticket promedio más alto.
"""

# Calcular el gasto promedio por tipo de cliente
avg_spent_by_customer = df.groupby("Customer type")["Total"].mean().sort_values(ascending=False)

# Gráfico de gasto promedio por tipo de cliente
plt.figure(figsize=(8, 5))
sns.barplot(x=avg_spent_by_customer.index, y=avg_spent_by_customer.values, palette="coolwarm")
plt.title("Gasto Promedio por Tipo de Cliente", fontsize=14)
plt.xlabel("Tipo de Cliente")
plt.ylabel("Gasto Promedio ($)")
plt.show()

"""
Análisis del Gasto por Tipo de Cliente
Los clientes "Member" gastan más en promedio que los clientes "Normal".
Esto sugiere que los clientes leales tienen un ticket de compra más alto, posiblemente debido a programas de fidelización o beneficios exclusivos.
"""

# Calcular el gasto promedio por método de pago
avg_spent_by_payment = df.groupby("Payment")["Total"].mean().sort_values(ascending=False)

# Gráfico de gasto promedio por método de pago
plt.figure(figsize=(8, 5))
sns.barplot(x=avg_spent_by_payment.index, y=avg_spent_by_payment.values, palette="muted")
plt.title("Gasto Promedio por Método de Pago", fontsize=14)
plt.xlabel("Método de Pago")
plt.ylabel("Gasto Promedio ($)")
plt.show()

"""
 Análisis del Gasto por Método de Pago
Los clientes que pagan con "Credit Card" tienen el gasto promedio más alto.
Los pagos en "Ewallet" y "Cash" tienen montos similares, pero ligeramente más bajos.
Esto sugiere que los clientes que usan tarjetas de crédito pueden estar comprando más o adquiriendo productos de mayor valor.
"""

# Calcular el total de ventas por categoría de producto
sales_by_product_line = df.groupby("Product line")["Total"].sum().sort_values(ascending=False)

# Gráfico de ingresos por categoría de producto
plt.figure(figsize=(10, 6))
sns.barplot(y=sales_by_product_line.index, x=sales_by_product_line.values, palette="coolwarm")
plt.title("Ingresos Totales por Categoría de Producto", fontsize=14)
plt.xlabel("Ingresos Totales ($)")
plt.ylabel("Categoría de Producto")
plt.show()

"""
Análisis de Ingresos por Categoría de Producto
"Food and Beverages" es la categoría con mayores ingresos, seguida por "Fashion Accessories".
"Health and Beauty" genera los menores ingresos, lo que indica que este segmento podría tener menor demanda o ticket promedio más bajo.
Esto sugiere que la tienda podría enfocar promociones en productos de menor venta para equilibrar ingresos.
"""

# Calcular la correlación entre cantidad comprada y monto total gastado
correlation = df[['Quantity', 'Total']].corr()

# Gráfico de dispersión entre cantidad y total gastado
plt.figure(figsize=(8, 5))
sns.scatterplot(x=df['Quantity'], y=df['Total'], alpha=0.5, color="blue")
plt.title("Relación entre Cantidad Comprada y Total Gastado", fontsize=14)
plt.xlabel("Cantidad Comprada")
plt.ylabel("Total Gastado ($)")
plt.show()

# Mostrar la correlación
correlation

"""
Análisis de la Correlación entre Cantidad Comprada y Total Gastado
Existe una correlación positiva fuerte (0.705) entre la cantidad de productos comprados y el total gastado.
Esto indica que a medida que los clientes compran más unidades, el monto total de su compra aumenta significativamente.
El gráfico de dispersión muestra que las compras de mayor cantidad tienden a tener valores altos en el total gastado.
"""

# Agregar una nueva columna con el día de la semana
df["Day of Week"] = df["Date"].dt.day_name()

# Agrupar ventas totales por día de la semana
sales_by_day = df.groupby("Day of Week")["Total"].sum()

# Ordenar los días de la semana correctamente
days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
sales_by_day = sales_by_day.reindex(days_order)

# Gráfico de ventas por día de la semana
plt.figure(figsize=(10, 5))
sns.barplot(x=sales_by_day.index, y=sales_by_day.values, palette="coolwarm")
plt.title("Tendencias de Ventas por Día de la Semana", fontsize=14)
plt.xlabel("Día de la Semana")
plt.ylabel("Ventas Totales ($)")
plt.xticks(rotation=45)
plt.show()

# Agrupar ventas por mes
df["Month"] = df["Date"].dt.month_name()
sales_by_month = df.groupby("Month")["Total"].sum()

# Ordenar los meses en orden cronológico
month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
sales_by_month = sales_by_month.reindex(month_order)

# Gráfico de ventas por mes
plt.figure(figsize=(10, 5))
sns.barplot(x=sales_by_month.index, y=sales_by_month.values, palette="muted")
plt.title("Tendencias de Ventas por Mes", fontsize=14)
plt.xlabel("Mes")
plt.ylabel("Ventas Totales ($)")
plt.xticks(rotation=45)
plt.show()

"""
Análisis de Tendencias de Ventas a lo Largo del Tiempo
Ventas por Día de la Semana:
Los días con mayor volumen de ventas son los viernes y sábados.
Los días con menor volumen de ventas son los lunes y martes.
Ventas por Mes:
Se observa un aumento en las ventas en la segunda mitad del mes, posiblemente debido a quincenas o promociones.
Las ventas tienden a estabilizarse a finales de mes.
"""

"""
Conclusiones y Recomendaciones Estratégicas

Optimización de Horarios y Promociones

Incrementar ofertas los días de menor venta (lunes y martes) para distribuir mejor el flujo de clientes.

Aprovechar los picos de venta en fines de semana para maximizar ingresos con estrategias de marketing.

Enfoque en Métodos de Pago y Clientes

Fomentar el uso de tarjetas de crédito, ya que los clientes que pagan con este método gastan más en promedio.

Premiar la fidelidad de los clientes “Member”, pues su gasto promedio es mayor que los clientes normales.

Estrategia de Productos

Reforzar la promoción de la categoría “Health and Beauty”, ya que tiene menores ventas en comparación con otras categorías.

Maximizar el inventario de “Food and Beverages”, la categoría más rentable.

Optimización de Personal y Logística

Asegurar mayor disponibilidad de personal en horarios pico (12:00 - 14:00 y 18:00 - 20:00).

Ajustar la reposición de inventario en función de las tendencias de ventas por día y categoría de producto.
"""
