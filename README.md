# Репозиторий Data-Science

Репозиторий содержит проекты связаные с **Data-Science** и анализом данных. 

Для каждого проекта созданна отдельная папка, содержащая проект в формате `'.ipynb'` и файл `'README.md'`. В файле 'README.md' отражено описание соответствующего проекта.  

Проекты написаны на языке программирования `Python 3.*` с использованием Jupyter Notebook.

# Содержание

## Анализ временного ряда оператора сотовой связи

Осуществлена детекция аномалий временного ряда и построен прогноз на следующие сутки
<br>`adtk` `datetime` `numpy` `matplotlib` `pandas` `pmdarima` `prophet` `pylab` `seaborn` `scikit-learn` `statsmodels`

## Анализ факторов, определяющих успешность игр

Выявление закономерностей, определяющих успешность игры, как основа для планирования кампании на 2017 год
<br>`pandas` `numpy` `matplotlib` `scipy` `seaborn` 

## Выбор региона перспективного для добычи нефти

В проекте осуществляется выбор регион, где добыча принесёт наибольшую прибыль на основе предсказаний о запасе нефти
<br>`pandas` `numpy` `matplotlib` `seaborn` `scikit-learn`

## Классификация комментариев (анализ тональности)

В проекте осуществляется анализ тональности текстов с применением моделей DistillBERT, логистической регрессии и градиентного бустинга
<br>`pandas` `numpy` `matplotlib` `seaborn` `scikit-learn` `DistillBERT` `CatBoost` `XGBoost` `LightGBM` `re` `nltk` `torch` `transformers` `tqdm` `wordcloud` 

## Определение возраста клиентов по изображению

Создана нейронная сеть, которая определяет возраст клиентов по фотографии с заданной точностью
<br>`pandas` `numpy` `matplotlib` `seaborn` `tensorflow` `keras`

## Отток клиентов банка

В проекте осуществляется прогноз оттокка клиентов банка на основе информации о 10 тысячах клиентов банка с целью определения дальнейшей стратегии компании
<br>`pandas` `scikit-learn` `matplotlib` `scipy` `seaborn` `warnings` `itertools`

## Прогноз оттока клиентов оператора связи

В проекте осуществляется прогноз оттокка клиентов оператора связи с реализацией [web-интерфейса](https://forecasting-the-outflow-of-telecom-customersclient-flo-7wjae1.streamlitapp.com/) и [дашборда](https://public.tableau.com/app/profile/danil2407/viz/2_16630961409680/sheet6?publish=yes)
<br>`numpy` `matplotlib` `pandas` `re` `seaborn` `scikit-learn` `catboost`

## Прогнозирование заказов такси

В проекте осуществляется количества заказов такси на следующий час
<br>`pandas` `numpy` `matplotlib` `seaborn` `scikit-learn` `statsmodels` `catboost`

## Forecasting_the_outflow_of_telecom_customers

В директории содержатся файлы необходимые для развертывания web-интерфейса к проекту - "Прогноз оттока клиентов оператора связи"