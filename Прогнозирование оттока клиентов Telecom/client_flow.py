# Импорт библиотек
import pandas as pd
import streamlit as st
import joblib
from data_preprocessing import Processing
from PIL import Image

# Добавление иконки сайта и изображения
st.set_page_config(page_icon="🏧", page_title="Client_outflow")
image = Image.open(r'img.png')
st.image(image)
st.title('Прогноз оттока клиентов')

# Зададим название файла с параметрами модели
# joblib_file = 'joblib_cbc.pkl'
joblib_file = r'joblib_cbc.pkl'

# Функция для загрузки данных
def load_data():
    uploaded_file = st.file_uploader(label='Выберите данные для классификации', type=['csv'])
    if uploaded_file is not None:

        return pd.read_csv(uploaded_file)
    else:
        return None

df = load_data()



if df is not None:
    # Обработаем данные
    # Инициализируем объект класса Processing
    proc = Processing()

    # Создадим список признаков, которые необходимо убрать из выборки
    delete_features = ['begin_date', 'day', 'month', 'year', 'end_date', 'lifetime_m', 'total_charges']

    # Проведем обработку
    test = proc.entire_graph(df, delete_features)

    # Загрузим параметры модели с помощью инструмента load библиотеки joblib
    joblib_cbc = joblib.load(joblib_file)

    # Сделаем предсказание
    joblib_cbc_predict = joblib_cbc.predict(test)

    # Добавим необходимые кнопки
    if st.button('Отобразить данные до преобразования'):
        st.dataframe(df)
        if st.button('Скрыть данные'):
            st.dataframe(df)
    if st.button('Отобразить данные после преобразования'):
        st.dataframe(test)
        if st.button('Скрыть данные'):
            st.dataframe(test)
    if st.button('Показать результаты классфикации'):
        st.markdown('# Результаты классификации')
        st.markdown('- 0 - клиент останется')
        st.markdown('- 1 - расторгнет договор')
        results = pd.DataFrame({'result':joblib_cbc_predict}, index=test.index)
        st.dataframe(results)
        if st.button('Скрыть результаты'):
            st.dataframe(test)

