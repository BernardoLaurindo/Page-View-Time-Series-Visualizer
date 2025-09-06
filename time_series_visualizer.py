import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Lê o arquivo CSV, converte a coluna 'date' para datetime e define como índice do DataFrame
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates = ['date'], index_col = 'date')

# Filtra os outliers
df = df[
    (df['value'] >= df['value'].quantile(0.025)) & # mantém valores maiores ou iguais ao percentil 2.5
    (df['value'] <= df['value'].quantile(0.975))   # mantém valores menores ou iguais ao percentil 97.5
]


def draw_line_plot():
    fig, ax = plt.subplots(figsize = (12, 6)) # figura com 12x6 de tamanho
    
    # Plota a série temporal: x = datas (índice), y = número de page views
    ax.plot(df.index, df['value'], color = 'red') # linha vermelha
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019') # título do gráfico
    ax.set_xlabel('Date') # rótulo do eixo x
    ax.set_ylabel('Page Views') # rótulo do eixo y
    fig.savefig('line_plot.png') # salva em line_plot.png
    return fig # retorna para os testes

def draw_bar_plot():
    df_bar = df.copy() # copia do DataFrame filtrado
    df_bar['year'] = df_bar.index.year # coluna com o ano (int)
    df_bar['month'] = df_bar.index.month_name() # coluna com o nome do mês (ex: January)

    # Agrupa por ano e mês e calcula a média de page views para cada grupo
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack() # tabela com anos nas linhas e meses nas colunas

    # Garante a ordem correta das colunas 
    df_grouped.columns = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Plota o DataFrame agrupado como gráfico de barras por ano
    fig = df_grouped.plot(kind = 'bar', figsize = (12, 6)).get_figure() # retorna o objeto figura do matplotlib
    plt.xlabel('Years') # rótulo do eixo x
    plt.ylabel('Average Page Views') # rótulo do eixo y
    plt.legend(title = 'Months') # legenda com título

    # Salva e retorna figura
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    df_box = df.copy() # copia para não alterar df original
    df_box.reset_index(inplace=True) # Transforma o índice 'date' em coluna normal para extrair ano e mês
    df_box['year'] = [d.year for d in df_box.date] # extrai ano de cada data
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Define a ordem dos meses
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Cria figura com 2 subplots lado a lado (1 linha, 2 colunas)
    fig, axes = plt.subplots(1, 2, figsize = (15, 6)) # axes[0] = box por ano, axes[1] = box por mês

    sns.boxplot(x = 'year', y = 'value', data = df_box, ax = axes[0]) # plota boxplot agrupado por ano
    axes[0].set_title('Year-wise Box Plot (Trend)') # título do primeiro subplot
    axes[0].set_xlabel('Year') # rótulo do eixo x do primeiro subplot
    axes[0].set_ylabel('Page Views') # rótulo do eixo y do primeiro subplot

    sns.boxplot(x = 'month', y = 'value', data = df_box, order = month_order, ax = axes[1]) # plota com meses na ordem correta
    axes[1].set_title('Month-wise Box Plot (Seasonality)') # título do segundo subplot
    axes[1].set_xlabel('Month') # rótulo do eixo x do segundo subplot
    axes[1].set_ylabel('Page Views') # rótulo do eixo y do segundo subplot

    # Salva e retorna a figura que tem os dois box plots
    fig.savefig('box_plot.png')
    return fig

    if __name__ == '__main__':
        draw_line_plot() # gera e salva o gráfico de linha
        draw_bar_plot() # gera e salva o gráfico de barras
        draw_box_plot() # gera e salva os box plots

