from flask import render_template, request, flash, redirect
from selenium import webdriver
import pyautogui
import time
from models import Torrent
from page import app

endereco = []


@app.route('/')
def installer():
    return render_template('instalador.html')


@app.route('/index')
def inicio():
    return render_template('home.html')


@app.route('/buscar', methods=['POST', ])
def busca():
    nome = request.form['nome']
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.implicitly_wait(10)
    driver.get('https://thepiratebay.org/')
    driver.implicitly_wait(3)
    write = driver.find_element_by_xpath('//*[@id="inp"]/input')
    write.send_keys(nome)
    driver.find_element_by_xpath('//*[@id="subm"]/input[1]').click()
    driver.implicitly_wait(2)
    erro = driver.find_element_by_xpath('/html/body/h2').text
    if 'Try adding an asterisk' in erro:
        flash('Nenhum resultado encntrado! Tente novamente.')
        driver.close()
        return redirect('/index')
    url = driver.current_url
    endereco.append(url)
    list_obj = []
    for c in range(1, 11):
        parcial_xpath = f'//*[@id="searchResult"]/tbody/tr[{c}]/td[2]/div/a'
        se = f'//*[@id="searchResult"]/tbody/tr[{c}]/td[3]'
        try:
            result = Torrent(c, driver.find_element_by_xpath(parcial_xpath).text,
                             driver.find_element_by_xpath(se).text)
            list_obj.append(result)
        except:
            print('--')
    driver.close()
    return render_template('buscador.html', lista=list_obj)


@app.route('/selecionar', methods=['POST', ])
def selecionar():
    numero_escolhido = request.form['nome']
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.implicitly_wait(3)
    driver.get(endereco[0])
    driver.find_element_by_xpath(f'//*[@id="searchResult"]/tbody/tr[{numero_escolhido}]/td[2]/div/a').click()
    time.sleep(10)
    pyautogui.hotkey("ctrl", "w")
    driver.find_element_by_xpath('//*[@id="details"]/div[3]/div[1]/a[1]').click()
    time.sleep(10)
    pyautogui.hotkey("ctrl", "w")
    pyautogui.press('left')
    pyautogui.press('enter')
    driver.close()
    '''time.sleep(15)
    for tab in range(1, 52):
        pyautogui.press('tab')
    pyautogui.press('enter')'''
    return render_template('formato.html')
