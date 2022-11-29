import calendar 
import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt



def client_df(df,ID):
    return df[df.ID_CLIENTE==ID]


def arange_df(df):
    df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y')
    df.sort_values('FECHA',inplace=True)
    return df 


def monthly_balance(df):
    "Function that sums all transactions in each month and displays a barplot"
    balance = df.groupby(df.FECHA.dt.month)['CANTIDAD'].sum().to_numpy()

    #automatically sets color based on net profit or net loss for the month 
    profit_color = [{mes<0: 'coral',  mes>0: 'cornflowerblue'}[True] for mes in balance]
    edges = [{mes<0: 'brown',  mes>0: 'mediumblue'}[True] for mes in balance]
    
    plt.figure(figsize=(10,5))
    plt.rcdefaults()
    plt.title('Ingresos netos mensuales',fontsize=20)
    plt.ylabel('€ (euros)',fontsize=20)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.bar(x = ['Enero','Febrero','Marzo','Abril','Mayo','Junio'],
            height=balance,
            color = profit_color,
            edgecolor=edges,
            linewidth=2)
    plt.axhline(color='black',
            linewidth=0.5)
    plt.axis('auto')
    

    plt.show()

    return 


def merge(df,dictionary,column):
    return pd.merge(df,dictionary,on=column)


def prescindibles_vs_imprescindibles(df,dictionary):
    "Function that sums transactions grouped by agrup_debito and displays a pie chart"

    df = merge(df,dictionary,'TAG_DEBITO_ID')
    gastos = abs(df.groupby(df.agrup_debito)['CANTIDAD'].sum().to_numpy())
    labels = ['Imprescindibles','Prescindibles']
    explode = (0.3, 0.1) 

    #some clients do not present 'gastos prescindibles' 
    if len(gastos)!= len(labels):
        print('¡Enhorabuena, no tienes gastos prescindibles!')
    
    else: 
        fig1, ax1 = plt.subplots()
        ax1.pie(gastos, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()

    return 


def simple_evolution(df):
    sns.set_theme()
    sns.set_context("notebook", font_scale=1, rc={"lines.linewidth": 4})
    plt.ylabel('Saldo (€)',fontsize=20)
    plt.xlabel('Fecha', fontsize=16)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=15)

    sns.lineplot(data=df,x='FECHA',y='SALDO_CUENTAS')

    return 


def nombre_gastos(df,dictionary,month):
    "Function that groups spendings by 'nombre' and displays a pie chart"

    df = merge(df,dictionary,'TAG_DEBITO_ID')
    gastos = abs(df[df.FECHA.dt.month==int(month.value)].groupby('nombre')['CANTIDAD'].sum().to_numpy()) 
    labels = df[df.FECHA.dt.month==int(month.value)].groupby('nombre')['CANTIDAD'].sum().index.to_list()
    explode = np.linspace(0,0.4,len(labels)) 

    if len(gastos)!= len(labels):
        print('Algo no cuadra')
    
    else: 

        fig1, ax1 = plt.subplots()
        plt.title('Spendings during '+calendar.month_name[int(month.value)],
                fontsize=20)
        ax1.pie(gastos, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


        plt.show()

    return 


def evolution_of_months(df):
    "Function that constructs monthly arrays with the cumulative spendings and displays plot"
    
    df['month'] = df.FECHA.dt.month #new column with just the month info 
    gastos = [] #this will contain 6 np arrays with all spendings in absolute value and cumsumed
    fechas = [] #this will contain the date for each one of the spendings 
    for month in df.month.unique(): 
        gastos.append(abs(df[(df['month']==month)&(df['CANTIDAD']<0)].CANTIDAD.to_numpy()).cumsum())
        fechas.append(df[(df['month']==month)&(df['CANTIDAD']<0)].FECHA.dt.day.to_numpy())
    
    gastos_final = []
    fechas_final=[]
    #here I take care of the last value and make it constant until day 31st of the month 
    for el in gastos:
        gastos_final.append(np.append(el,el[len(el)-1]))
    for el in fechas:
        fechas_final.append(np.append(el,31))

    i=0
    for el in gastos_final:
        plt.plot(fechas_final[i],el,label=calendar.month_name[i+1])
        i += 1
    plt.legend(loc=(1.01, 0.63))
    plt.ylabel('Gasto acumulado',fontsize=20)
    plt.xlabel('Día del mes', fontsize=20)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)