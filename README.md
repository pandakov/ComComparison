<p align="center">
  <img src="https://tools.pixelplus.ru/images/1647520977image1.png" align="middle"  width="600" />
</p>


<h2 align="center">
  ComComparison
</h2>

<h4 align="center">

![1](https://img.shields.io/badge/python-3.10.6+-aff.svg)
![2](https://img.shields.io/badge/os-linux%2C%20win%2C%20mac-pink.svg)
![3](https://img.shields.io/github/stars/pandakov/ComComparison?color=ccf)
![4](https://img.shields.io/github/v/release/pandakov/ComComparison?color=ffa)

</h4>

-----------------------------------------------

<h4 align="center">
  <a href=#features> Features </a> |
  <a href=#installation> Installation </a> |
  <a href=#quick-start> Quick Start </a> |
  <a href=#community> Community </a>
</h4>

-----------------------------------------------

**ComComparison** это *простая в использовании* и *мощная* командная строка. Готовое решение для вас!



## &#128204;Features

### &#128642;Под капотом  (Мы предоставляем сценарий):
* Внесение своей базы данных  &#128194;
* Очистка базы данных 	&#9986;
* Векторизация &#128207;
* Классификация &#128065;
* Логистическая регрессия &#128172;
* Ранжирование &#9203;
* Вывод топ-10 компаний со оенкой схожести  &#128161;


###  	&#128270; Нейронная поисковая система
Выполнен в стиле классического браузерного поисковика. Позволяет вывести все созвучные организации.
```python
Введите название компании:
>>>
```

#### ❓ Настройка подготовки данных

Для тренировки модели можно использовать удобный папплайн `train.py`
```python
# Generate PRE pipeline
pipe_pre = Pipe(
    TextTransform.to_lower_case(),
    TextTransform.drop_char(chars=r".,()0123456789«»$^#№"),
    TextTransform.drop_char(chars=r'-*"/&+:;@=\|?!' + r"'", replace=" "),
    TextTransform.drop_words(words=drop_ownership_list),
    TextTransform.drop_words(words=drop_countries_list),
    TextTransform.drop_whitespaces(),
    TextTransform.transliterate(),
)
```

#### 💌 NLTK и spaCy 

Пункт в разработке


#### ⚡ Пример работы

```python
Введите название компании:
bridgestone

Топ 10 похожих компаний:
1: Zeon Research Vietnam Co., Ltd; вероятность дубля: 1.0
2: Bridgestone India; вероятность дубля: 1.0
3: Bridgestone International Group; вероятность дубля: 1.0
4: Bridgestone De Mexico S.A. De C.V.; вероятность дубля: 1.0
5: Bridgestone De Costa Rica S.A.; вероятность дубля: 1.0
6: Bridgestone India Pvt., Ltd.; вероятность дубля: 1.0
7: Bridgestone Canada Inc.; вероятность дубля: 1.0
8: Bridgestone Firestone De Mexico Sa De Cv; вероятность дубля: 0.99
9: Bridgestone Neumaticos De; вероятность дубля: 0.99
10: Michelin Americas Research; вероятность дубля: 0.99
```

```python
Введите название компании:

pir

Похожих компаний нет в списке или введены кракозябры
```

```python
Введите название компании:

dsfhsdhsdhdfh

Похожих компаний нет в списке или введены кракозябры
```


#### 🚀 Метрики

Представлены метрики качества модели (логистической регрессии) в зависимости от
метода векторизации и факта очистки датасета

|                     | f1   | f1-macro | recall | roc-auc |
|---------------------|------|----------|--------|---------|
| tf-idf              | 0.40 | 0.69     | 0.28   | 0.96    |
| tf-idf +  очистка   | 0.73 | 0.86     | 0.65   | 0.96    |
| word2vec            | 0.42 | 0.71     | 0.29   | 0.93    |
| word2vec +  очистка | 0.52 | 0.76     | 0.37   | 0.93    |

## &#128204;Installation

### Используемые библиотеки

* python >= 3.10
* numpy >= 1.23.4
* pandas >= 1.5.0
* scikit-learn >= 1.1.2
* notebook >= 6.5.1
* tables >= 3.7.0
* gensim >= 4.2.0
* nltk >= 3.6.5
* joblib >= 1.1.0

Через requirements.txt для pip:
```python
pip install -r requirements.txt
```
С помощью [Poetry](https://python-poetry.org) устанавливаются все зависимости. Кроме pip можно использовать [Homebrew](https://formulae.brew.sh/formula/poetry) или [Conda](https://anaconda.org/conda-forge/poetry).
``` python
git clone https://github.com/pandakov/ComComparison.git
pip install poetry
poetry install
```


## &#128204; Quick Start
> Сценарий 1 - Обучаем на ваших данных
 
 
 
В папку `/data` добавляете свой `train.csv`

```python
>>>train()
>>>ranking()
```
Программа формирует файлы весов(`embeddings.h5`, `logit.joblib`, `word2vec.model`) и добавляет в `/data`.
Трейн лежит на [диске](https://drive.google.com/file/d/1e9bdr7wcQX_YBudQcsKj-sMoIGxQOlK4/view)

> Сценарий 2 - используем наши веса

В папку `/data` добавляете свой `embeddings.h5`, `logit.joblib`, `word2vec.model`

```python
>>>ranking()
```
Они лежать на [диске](https://drive.google.com/drive/folders/1b3BEHNyzqOKzoOP4HaH4zU5SXu3_lwOD?usp=sharing)

## &#128204;Community

### Расти вместе с AI Talent Hub!
На базе [AI Talent Hub](https://ai.itmo.ru/) Университет ИТМО совместно с компанией Napoleon IT запустил образовательную программу «Инженерия машинного обучения». Это не краткосрочные курсы без практического применения, а онлайн-магистратура нового формата, основанная на реальном рабочем процессе в компаниях.

Этот проект создан в рамках второго задания по курсу: "Глубокое обучение на практике"

Мы команда ViN:
* [Виктор](https://t.me/anoninf)
* [Илья](https://t.me/sadinhead)
* [Никита](https://t.me/space_apple)

<details><summary> &#128516; Шутейка </summary>
<p>

![Jokes Card](https://readme-jokes.vercel.app/api)

</p>
</details>

## Цитирование 

Если вы используете ComComparison в своих исследованиях, рассмотрите возможность цитирования
```python
@misc{=comComparison,
    title={ComComparison: An Easy-to-use and High Performance CLI},
    author={ViN Contributors},
    howpublished = {\url{https://github.com/pandakov/ComComparison}},
    year={2022}
}
```

## Благодарность

- [NLP. Основы. Техники. Саморазвитие. Часть 1](https://habr.com/ru/company/abbyy/blog/437008/)
- [NLP. Основы. Техники. Саморазвитие. Часть 2: NER](https://habr.com/ru/company/abbyy/blog/449514/)
- [Как найти что-то в тексте](https://habr.com/ru/post/530878/)
- [SpaCy](https://nlpub.ru/SpaCy)
- [NLTK](https://nlpub.ru/NLTK)
- [Сравниваем работу open source Python — библиотек для распознавания именованных сущностей](https://habr.com/ru/post/502366/)
## Лицензия

 [The MIT License](https://opensource.org/licenses/mit-license.php).