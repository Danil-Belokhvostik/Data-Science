# Импорт библиотек
import pandas as pd
import streamlit as st
import pickle
from data_preprocessing import Processing
# import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns
# from PIL import Image
# import altair as alt

# Зададим конфигурацию страницы
st.set_page_config(
    page_icon="💰",
    page_title="Client_outflow",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Danil-Belokhvostik/Data-Science/tree/\
        main/Прогноз%20оттока%20клиентов%20оператора%20связи',
        'About': "В проекте осуществляется прогноз оттокка клиентов оператора связи с реализацией web-интерфейса"})

# Загрузим фоновое изображение и выведем название
st.image('Forecasting_the_outflow_of_telecom_customers/img.jpg')
# st.image('img.jpg')
st.title('Прогноз оттока клиентов')

# Зададим название файла с параметрами модели
joblib_file = 'Forecasting_the_outflow_of_telecom_customers/pickle_model.pkl'
# joblib_file = 'pickle_model.pkl'


def load_data():
    uploaded_file = st.file_uploader(label='Выберите данные для классификации', type=['csv'])
    if uploaded_file is not None:

        return pd.read_csv(uploaded_file)
    else:
        return None

# Функция для создания предсказания
def predict(df):
    # Обработаем данные
    # Инициализируем объект класса Processing
    proc = Processing()

    # Создадим список признаков, которые необходимо убрать из выборки
    delete_features = ['begin_date', 'day', 'month', 'year', 'end_date', 'lifetime_m', 'total_charges']

    # Проведем обработку
    df_proc = proc.entire_graph(df, delete_features)

    # Загрузим параметры модели с помощью инструмента load библиотеки joblib
    joblib_cbc = pickle.load(open(joblib_file, 'rb'))

    # Сделаем предсказание
    joblib_cbc_predict = joblib_cbc.predict(df_proc)

    # Сформируем датафрейм с предсказаниями
    results = pd.DataFrame({'result': joblib_cbc_predict}, index=df_proc.index)
    return results, df_proc

# Функция для отображения исходных данных и результатов обработки и прогнозирования
def results_displaying(data, proc_data, result, hist_choice):

    data_before_proc = st.expander('Отобразить данные до преобразования')
    # if st.button('Отобразить данные до преобразования'):
    with data_before_proc:
        st.dataframe(data)

    data_after_proc = st.expander('Отобразить данные после преобразования')
    with data_after_proc:
        st.dataframe(proc_data)

    st.markdown('# Результаты классификации')
    # Создадим столбцы для результатов и гистограммы
    col1, col2, col3 = st.columns(3)

    with col1:

        show_result = st.expander('Показать результаты классфикации 👉')

        with show_result:

            st.markdown('- 0 - клиент останется')
            st.markdown('- 1 - расторгнет договор')
            st.dataframe(result)


    with col3:

        show_result = st.expander('Диаграмма распределения целевого класса')
        with show_result:

            if hist_choice == 'Отобразить':

                sns.set_theme(context='talk', style='darkgrid', palette='pastel')
                fig = Figure(figsize=(10, 10))
                ax = fig.subplots()
                sns.histplot(result,
                             x='result',
                             hue='result',
                             palette='deep',
                             ax=ax,
                             discrete=True
                             )
                ax.set_xticks([0, 1])
                ax.set_xlabel('Статус клиентов')
                ax.set_ylabel('Количество')
                ax.legend(['Клиент расторгнет договор', 'Клиент останется'])
                st.pyplot(fig)

    # Скачивание результатов
    csv = convert_df(result)
    st.download_button(
        label="⬇️Скачать результаты классификации",
        data=csv,
        file_name='Результаты классфикации.csv',
        mime='text/csv')

@st.cache
def convert_df(results):
    return df.to_csv().encode('utf-8')

# Создадим колонки, чтобы уместить кнопки загрузки в левой части экрана
start_col1, start_col2, start_col3 = st.columns(3)

with start_col1:

    # Загрузим данные
    df = load_data()

    # Предоставим возможность использовать пример исходного файла
    # Добавим кнопку
    use_example_file = st.checkbox(
        "Use example file", False, help="Use in-built example file to demo the app"
    )

    # Добавим действие, если кнопка активирована
    if use_example_file:
        # uploaded_file = "telecom_cut_samle_features.csv"
        uploaded_file = "Forecasting_the_outflow_of_telecom_customers/telecom_cut_samle_features.csv"
        df = pd.read_csv(uploaded_file)
        st.success("Данные загружены и обрбаботаны")

    elif df is not None:
        st.success("Данные загружены и обрбаботаны")

    else:
        st.error("Скачать пример исходного файла можно по ссылке"
                 "(https://clck.ru/sdPMe)")

# Настроим боковую панель
if df is not None:

    results, df_proc = predict(df)

    if results is not None:

        # Добавим боковую панель
        st.sidebar.markdown("## Задайте параметры преобразований")

        # Выбор отображаемых клиентов
        clients = list(df['customerID'].unique())
        clients.insert(0, 'Все клиенты')
        client_choice = st.sidebar.selectbox("Выберете клиента", clients)

        # Отображение гистограммы
        hist_answer = ['Отобразить', 'Не отображать']
        hist_choice = st.sidebar.selectbox("Нужна ли гистограмма", hist_answer)

        if client_choice == 'Все клиенты':
            results_displaying(df, df_proc, results, hist_choice)
        else:
            df_client_index = list(df.customerID).index(client_choice)
            results_displaying(df[df.index == df_client_index],
                               df_proc[df_proc.index == client_choice],
                               results[results.index == client_choice],
                               hist_choice)