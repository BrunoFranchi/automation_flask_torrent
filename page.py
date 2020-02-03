from flask import Flask, render_template, request, flash, redirect, session
from selenium import webdriver
app = Flask(__name__)

endereco = []


@app.route('/')
def inicio():
    return render_template('home.html')


@app.route('/buscar', methods=['POST', ])
def busca():
    nome = request.form['nome']
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.implicitly_wait(10)
    driver.get('http://www.filmesviatorrents.info/')
    driver.implicitly_wait(3)
    driver.find_element_by_name('s').click()
    write = driver.find_element_by_name('s')
    write.send_keys(nome)
    driver.find_element_by_name('s').submit()
    url = driver.current_url
    endereco.append(url)
    driver.implicitly_wait(3)
    results = []
    for c in range(5, 20):
        parcial_xpath = f'//*[@id="mainWrapper"]/div/div[{c}]/h2/a'

        try:
            results.append(str(c).upper() + ' -- ' + driver.find_element_by_xpath(parcial_xpath).text)
        except:
            print('--')
    driver.close()
    return render_template('buscador.html', lista=results)


@app.route('/selecionar', methods=['POST', ])
def selecionar():
    numero_escolhido = request.form['nome']
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.implicitly_wait(10)
    driver.get(endereco[0])
    driver.find_element_by_xpath(f'//*[@id="mainWrapper"]/div/div[{numero_escolhido}]/h2/a').click()
    driver.implicitly_wait(2)
    driver.find_element_by_xpath('//div/div/a/img').click()
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="botao"]').click()
    driver.implicitly_wait(15)
    print('cliquei')
    driver.find_element_by_xpath('//*[@id="botao2"]').click()
    driver.implicitly_wait(2)
    print('cliquei')

    print('encontrei')
    return render_template('formato.html')


app.run(debug=True)