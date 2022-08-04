# Импорт библиотек
import pandas as pd
import streamlit as st
import joblib
#import pickle
from data_preprocessing import Processing
from PIL import Image

# Добавление иконки сайта и изображения
st.set_page_config(page_icon="🏧", page_title="Client_outflow")
# image = Image.open('img.png')
# uploaded_img = st.file_uploader("img",type="jpg")
# st.open(uploaded_img)
# img = Image.open("https://github.com/Danil-Belokhvostik/Data-Science/blob/main/Forecasting_the_outflow_of_telecom_customers/img.jpg")
# st.image(img, width = 200 )
# st.image('https://github.com/Danil-Belokhvostik/Data-Science/blob/main/Forecasting_the_outflow_of_telecom_customers/img.jpg')
#image = Image.open('img.png')
#st.image(image)
st.title('Прогноз оттока клиентов')

# Зададим название файла с параметрами модели
# joblib_file = 'joblib_cbc.pkl'
# joblib_file = "joblib_cbc.pkl"
# joblib_file = 'joblib_cbc.pkl'



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
    uploaded_model = st.file_uploader(label='Выберите файл с моделью в формате - .pkl', type=['pkl'])
    if uploaded_model is not None:
        joblib_cbc = joblib.load(uploaded_model)

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

