# Импорт библиотек
import pandas as pd
import streamlit as st
import pickle
from data_preprocessing import Processing
from PIL import Image

# Зададим инконку сайта
st.set_page_config(page_icon="🏧", page_title="Client_outflow")

# Загрузим фоновое изображение и выведем название
st.image('Forecasting_the_outflow_of_telecom_customers/img.jpg')
st.title('Прогноз оттока клиентов')

# Зададим название файла с параметрами модели
joblib_file = 'Forecasting_the_outflow_of_telecom_customers/pickle_model.pkl'

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

    #joblib_cbc = joblib.load(joblib_file, 'rb')

    joblib_cbc = pickle.load(open(joblib_file, 'rb'))
    # Сделаем предсказание
    joblib_cbc_predict = joblib_cbc.predict(df_proc)

    # Сформируем датафрейм с предсказаниями
    results = pd.DataFrame({'result':joblib_cbc_predict}, index=df_proc.index)
    return results, df_proc

@st.cache
def convert_df(results):
     return df.to_csv().encode('utf-8')

# Загрузим данные
df = load_data()

# Настроим основные кнопки
if df is not None:

    
    results, df_proc = predict(df)

    if results is not None:
        
        st.success("Данные загружены и обрбаботаны")

        if st.button('Отобразить данные до преобразования'):
            st.dataframe(df)

            if st.button('Скрыть данные'):
                st.dataframe(df)

        if st.button('Отобразить данные после преобразования'):
            st.dataframe(df_proc)

            if st.button('Скрыть данные'):
                st.dataframe(df_proc)

        if st.button('Показать результаты классфикации'):
            st.markdown('# Результаты классификации')
            st.markdown('- 0 - клиент останется')
            st.markdown('- 1 - расторгнет договор')
            st.dataframe(results)

            if st.button('Скрыть результаты'):
                st.dataframe(results)

        # Скачивание результатов
        csv = convert_df(results)
        st.download_button(
            label="Скачать результаты классификации",
            data=csv,
            file_name='Результаты классфикации.csv',
            mime='text/csv')
else:
    st.error("С примером исходного файла можно ознакомиться по ссылке"
             "(https://clck.ru/sUL5Q)")
