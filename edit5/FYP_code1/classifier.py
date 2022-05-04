import pandas as pd
from pandas.api.types import CategoricalDtype
from statsmodels.miscmodels.ordinal_model import OrderedModel

df = pd.read_csv('train.csv')


def preprocessing():
    global df
    df.head()
    df['INTAKE_AIR_TEMP']=pd.to_numeric(df['INTAKE_AIR_TEMP'],errors='coerce')
    df = df.dropna()
    print("Preprocessing done")

def modelling():
    classify_type = CategoricalDtype(categories=['Good', 'Moderate', 'Bad'], ordered=True)
    df['RESULT'] = df['RESULT'].astype(classify_type)
    mod_prob = OrderedModel(df['RESULT'],
                            df[['INTAKE_AIR_TEMP', 'COOLANT_TEMPERATURE', 'ENGINE_RPM']],
                            distr='logit')
    res_log = mod_prob.fit(method='bfgs')
    print("Modelling Done")
    return res_log

def prediction(df):
    global res_log
    my_predicted = res_log.model.predict(res_log.params,
                                         exog=df[['INTAKE_AIR_TEMP', 'COOLANT_TEMPERATURE', 'ENGINE_RPM']])
    list1=my_predicted.tolist()
    return list1

def myfunc(intake_air,coolant,engine_rpm):

    data = {'INTAKE_AIR_TEMP': [intake_air],
            'COOLANT_TEMPERATURE': [coolant],
            'ENGINE_RPM': [engine_rpm]
            }
    df1 = pd.DataFrame(data)
    res_list=prediction(df1)
    elem = max(res_list[0])
    # index
    res = res_list[0].index(elem)
    return res


preprocessing()
res_log = modelling()
