import numpy as np
import pandas as pd
import re


class Processing:

    # Метод snake_case преобразует названия признаков
    # из CamelCase в snake_case
    def snake_case(self, df):
        # Создадим список названий признаков в формате python_case,
        # использовав интрумент sub из библиотеки re
        python_case = list(map(lambda x: re.sub(r'(?<!^)(?=[A-Z])', '_', x)
                               .lower(), df.columns))

        # Переименуем названия признаков, используя инструмент rename
        df = df.rename(columns=dict(zip(df.columns, python_case)))
        df = df.rename(columns={'customer_i_d': 'customer_id',
                                'streaming_t_v': 'streaming_tv'})
        # Вернем результат
        return df

    # Метод fill_nan обрабатывает пропущенные значения
    def fill_nan(self, df):
        # Заменим значения NaN, которые появились после объединения таблиц.
        # Эти значения соответствуют клиентам, использующим либо интернет, либо телефон,
        # но не все сразу
        internet_columns = ['internet_service', 'online_security',
                            'online_backup', 'device_protection',
                            'tech_support', 'streaming_tv',
                            'streaming_movies']
        df[internet_columns] = df[internet_columns].fillna('phone')

        # Также заменим NaN значения в поле multiple_lines.
        # Это клиенты, которые ипользуют только интернет.
        # Выведем уникальные значения до и после преобразований
        df['multiple_lines'] = df['multiple_lines'].fillna('internet')
        return df

    # Метод date_processing:
    # 1. преобразует соответствующие признаки в формат datetime64
    # 2. Создает дополнительные признаки
    def lifetime(self, df):
        # Заменим все значения "No" в поле "end_date" на дату выгрузки данных
        today = '2020-02-01 00:00:00'
        df['end_date'] = df['end_date'].apply(lambda x: today if x == 'No' else x)

        # Преобразуем столбцы к типу datetime
        df['end_date'] = pd.to_datetime(df['end_date'], format='%Y.%m.%d %H:%M:%S')
        df['begin_date'] = pd.to_datetime(df['begin_date'], format='%Y.%m.%d %H:%M:%S')

        # Рассчитаем продолжительность взаимодействия с компанией
        df['lifetime_d'] = (df['end_date'] - df['begin_date']).dt.days
        df['lifetime_m'] = (df['end_date'] - df['begin_date']) // np.timedelta64(1, 'M')

        # Метод diff_charges_lifetime создает признак diff_charges_lifetime,
        # который будет характеризовать разницу между количеством
        # месячных платежей и временем жизни клиента
        df['diff_charges_lifetime'] = ((df['total_charges'] // df['monthly_charges'])
                                       - df['lifetime_m']).astype('int64')

        # Создадим признаки year, month, day, содержащие год,
        # месяц и день оформления договора соответственно
        df['year'] = df['begin_date'].dt.year
        df['month'] = df['begin_date'].dt.month
        df['day'] = df['begin_date'].dt.day

        return df

    # Метод payment_characteristics создает признак с тем же названием,
    # в котором выделим три категории клиентов:
    # 1. debtor - не выплачивал два и более месяцев
    # 2. normal - допустимые выплаты
    # 3. overpayment - выплачивал два и более месяцев после расторжения договора
    def payment_characteristics(self, df):
        df['payment_characteristics'] = df['diff_charges_lifetime']
        for i in df['payment_characteristics']:
            if i <= -2:
                i = 'debtor'
            elif i >= 2:
                i = 'overpayment'
            else:
                i = 'normal'

        return df

        # Метод set_df_index установит в качестве индексов ID клиента

    def set_df_index(self, df):
        df = df.set_index('customer_id')
        return df

    # Метод entire_graph объединяет в себе все предыдущие методы класса
    # Удаляет переданный список признаков
    # Возвращает обработанный датасет
    def entire_graph(self, df, delete_features=[]):
        df = self.set_df_index(self.payment_characteristics(self.lifetime(self.fill_nan(self.snake_case(df)))))
        df = df.drop(delete_features, axis=1)
        return df
