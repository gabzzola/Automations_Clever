import pyautogui
import time
import pandas
import keyboard

pyautogui.PAUSE = 1

pyautogui.press('win')
pyautogui.write('chrome')
pyautogui.press('enter')

pyautogui.write('https://lachocolataria.webclever.com.br/#/login')
pyautogui.press('enter')

time.sleep(3)

# Removendo autopreenchimento do login
pyautogui.click(x=722, y=409)
pyautogui.hotkey('ctrl', 'a')
pyautogui.press('backspace')

# Login
pyautogui.write('clever')
pyautogui.press('tab')
pyautogui.write('Cl3v3r123')
pyautogui.press('tab')
pyautogui.press('enter')

time.sleep(3)

# Almoxarifado > Produtos 
pyautogui.click(x=345, y=154)
pyautogui.click(x=422, y=201)

# Lendo o arquivo de produtos no formato CSV 
table = pandas.read_csv("C:/Users/gazzo/OneDrive/Documents/GitHub/Automations_Python/Product-Registration/Pyautogui/produtos.csv")
print(table)

for row in table.index:
  # Descrição, valor de venda e observação da linha atual
  descricao = table.loc[row, 'descricao']
  observacao = table.loc[row, 'observacao']
  valor_de_venda = table.loc[row, 'valor_de_venda']

  # Formata descrição 
  descricao_formatado = descricao.upper()

  # Formata o valor de venda
  valor_de_venda_formatado = f'{valor_de_venda:.2f}'.replace('.', ',')

  # Botão adicionar
  pyautogui.click(x=1855, y=244)
  
  time.sleep(3)

  # Descrição
  pyautogui.click(x=522, y=328)
  keyboard.write(str(descricao_formatado))

  # Observação
  if not pandas.isna(observacao):
    pyautogui.click(x=95, y=752)
    keyboard.write(str(observacao))

  # Valor de venda
  pyautogui.click(x=1712, y=650)
  pyautogui.write(str(valor_de_venda_formatado))

  pyautogui.click(x=1702, y=910)

  time.sleep(3)