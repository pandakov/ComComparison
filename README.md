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

![taskflow1](https://user-images.githubusercontent.com/11793384/159693816-fda35221-9751-43bb-b05c-7fc77571dd76.gif)


#### ❓ Написать про пайплайн Виктора


We provide question answering pipeline which can support FAQ system, Document-level Visual Question answering system based on [🚀RocketQA](https://github.com/PaddlePaddle/RocketQA).

<div align="center">
    <img src="https://user-images.githubusercontent.com/11793384/168514868-1babe981-c675-4f89-9168-dd0a3eede315.gif" width="400">
</div>


#### 💌 Написать про nltk 

We build an opinion extraction system for product review and fine-grained sentiment analysis based on [SKEP](https://arxiv.org/abs/2005.05635) Model.

<div align="center">
    <img src="https://user-images.githubusercontent.com/11793384/168407260-b7f92800-861c-4207-98f3-2291e0102bbe.png" width="300">
</div>


#### ⚡ Пример работы

<div align="center">
    <img src="https://user-images.githubusercontent.com/11793384/168407921-b4395b1d-44bd-41a0-8c58-923ba2b703ef.png" width="400">
</div>

```python
AutoTokenizer.from_pretrained("ernie-3.0-medium-zh", use_faster=True)
```

Set `use_faster=True` to use C++ Tokenizer kernel to achieve 100x faster on text pre-processing. For more usage please refer to [FasterTokenizer](./faster_tokenizer).


#### 🚀 Метрики

<div align="center">
    <img src="https://user-images.githubusercontent.com/11793384/168515134-513f13e0-9902-40ef-98fa-528271dcccda.png" width="300">
</div>


For more super large-scale model pre-training details please refer to [GPT-3](./examples/language_model/gpt-3).

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

 Илюха напиши что-то да как. С нашей базой и с базой клиентов

```python
import ranking
from ranking import main 
import importlib
importlib.reload(ranking)

main()
>>> 
```

 Use `AutoModel` API to **⚡SUPER FAST⚡** download pretrained models of different architecture. 
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