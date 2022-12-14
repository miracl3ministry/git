import os
import time
import json
import shutil
import requests
from threading import Timer

def generateLand(data, language):
    """
    Генерация лендинга, на входе данные с формы, на выходе ссылки на предпросмотр
    """
    currentDirectory = os.getcwd()
    newFolderName = str(time.time_ns())
    copyFromPath = os.path.join(currentDirectory, 'models', 'template')
    copyToPath = os.path.join(currentDirectory, 'views/public/generated', newFolderName)
    os.mkdir(copyToPath)
    landPaths = [os.path.join(copyToPath, '0'), os.path.join(copyToPath, '1'), os.path.join(copyToPath, '2')]

    text = requestsToApi(data, language)
    saveTextLog(newFolderName, text, data)
    if (type(text) == 'list' and text['detail']): raise Exception(text['detail'])
    writeTxtFile(copyToPath, text, data['product_name'])
    createLand(copyFromPath, landPaths[0], text[0], data['product_name'])
    createLand(copyFromPath, landPaths[1], text[1], data['product_name'])
    createLand(copyFromPath, landPaths[2], text[2], data['product_name'])
    timer = Timer(86400.0, deleteLands, args=[copyToPath]) # 60 sec * 60 min * 24 hours = 86 400 sec
    timer.start()
    return [rf'static\generated\{newFolderName}\0\index.html', 
            rf'static\generated\{newFolderName}\1\index.html', 
            rf'static\generated\{newFolderName}\2\index.html',]

def deleteLands(pathToFolder):
    shutil.rmtree(pathToFolder)

def saveTextLog(name, text, req):
    logPath = os.path.join(os.getcwd(), 'models', 'logs', name)
    with open(logPath, "w", encoding='utf-8') as txtFile:
        data = {
            'request': req,
            'generated': text
        }
        txtFile.write(json.dumps(data, ensure_ascii=False))

def createZip(folderName, land):
    """
    Создание архива с лендингом для скачивания
    """
    pathToDirectory = os.path.join(os.getcwd(), 'views\public\generated', folderName)
    pathToLand = os.path.join(pathToDirectory, land)
    if (not os.path.exists(pathToLand)): raise Exception('Лендинг не найден')
    if (os.path.exists(os.path.join(pathToDirectory, f'{land}.zip'))): return "Архив существует"
    shutil.make_archive(pathToLand, 'zip', pathToLand)
    return "Готово, скачивай"

def writeTxtFile(copyToPath, text, productName):
    """
    Запись результатов в текстовый файл
    """
    with open(os.path.join(copyToPath, "text.txt"), "w", encoding='utf-8') as txtFile:
        data = text
        for item in data:
            item['productName'] = productName
        txtFile.write(json.dumps(data, ensure_ascii=False))

def createLand(copyFromPath, copyToPath, text, productName):
    """
    Подстановка сгенерированного текста в шаблон
    """
    shutil.copytree(copyFromPath, copyToPath)
    html = open(os.path.join(copyToPath,"index.html"), "r", encoding='utf-8').read()
    html = html.replace('{{product_name}}', productName
              ).replace('{{title}}', text['title']
              ).replace('{{subtitle}}', text['subtitle']
              ).replace('{{button}}', text['button']
              ).replace('{{main_feature_title}}', text['main_feature_title']
              ).replace('{{main_feature_subtitle}}', text['main_feature_subtitle']
              ).replace('{{feature_1_title}}', text['feature_1_title']
              ).replace('{{feature_1_subtitle}}', text['feature_1_subtitle']
              ).replace('{{feature_2_title}}', text['feature_2_title']
              ).replace('{{feature_2_subtitle}}', text['feature_2_subtitle']
              ).replace('{{feature_3_title}}', text['feature_3_title']
              ).replace('{{feature_3_subtitle}}', text['feature_3_subtitle']
              ).replace('{{cta}}', text['cta'])
    with open(os.path.join(copyToPath,"index.html"), "w", encoding='utf-8') as indexFile:
        indexFile.write(html)

def requestsToApi(payload, language):
    """
    Обращение к апи
    """
    # config = json.loads(open("config.json", "r").read())
    # url = f"https://api.writesonic.com/v1/business/content/landing-pages?engine={config['engine']}&language={language}"
    # headers = {
    #     "accept": "application/json",
    #     "content-type": "application/json",
    #     "X-API-KEY": config['apiKey']
    # }
    # response = requests.post(url, json=payload, headers=headers)
    # text = response.text


    text = '[{"title": "Получите лучшие возможности Google Chrome на своем рабочем столе\n", "subtitle": " С Google chrome вы больше никогда не потеряете свое место.", "main_feature_title": "Safari не идет ни в какое сравнение с Google Chrome.\n", "main_feature_subtitle": " Safari может быть вашим любимым браузером, но знаете ли вы, что это не Google chrome? Если вы пользуетесь браузером Google chrome, вам не придется беспокоиться о значительной производительности или проблемах совместимости. Присоединяйтесь к высшей лиге веб-пользователей и начните работать с лучшим браузером уже сегодня!", "feature_1_title": "Будьте на шаг впереди.\n", "feature_1_subtitle": " Будьте впереди всех с инструментами Google прямо в вашем браузере. С помощью Google chrome вы можете воспользоваться преимуществами автозаполнения, поиска и других функций в браузере, чтобы быть на шаг впереди своих конкурентов.", "feature_2_title": "Защитите свою конфиденциальность в Интернете с помощью Chrome.\n", "feature_2_subtitle": " Управляйте и контролируйте настройки безопасности в Интернете с помощью Google Chrome. Сохраните конфиденциальность своих данных с помощью новейших технологий браузера и перестаньте беспокоиться о хакерах.", "feature_3_title": "Браузер для современного мира.\n", "feature_3_subtitle": " Google chrome - лучший веб-браузер, с эффективными и простыми инструментами для работы в браузере. Благодаря таким функциям, как просмотр инкогнито и синхронизация между устройствами, вы легко справитесь с делами, когда находитесь в пути. В Chrome также встроены функции блокировки рекламы и защиты от вредоносных программ, что позволяет вам оставаться в безопасности во время просмотра веб-страниц.", "cta": "Google chrome - лучший веб-браузер.\n", "button": " Загрузите Google Chrome сегодня"}, {"title": "Google chrome - лучший веб-браузер\n", "subtitle": " Google chrome - лучший веб-браузер, потому что он сверхбыстрый, умный и интуитивно понятный. Гладкий интерфейс и мощные функции позволяют легко ориентироваться в Интернете с помощью Google Chrome.", "main_feature_title": "Просматривайте веб-страницы быстрее с помощью Google Chrome.\n", "main_feature_subtitle": " Google chrome - лучший веб-браузер для большинства людей, он быстрый и безопасный. С помощью Google chrome вы можете просматривать веб-страницы безопаснее, чем когда-либо прежде.\nОдним щелчком мыши можно открыть новую вкладку в google chrome, чтобы не отвлекаться от работы. В браузер также встроено расширение для покупок, которое позволяет совершать покупки в Интернете, не выходя из google chrome.", "feature_1_title": "Оставайтесь на связи с Интернетом.\n", "feature_1_subtitle": " Используйте такие инструменты Google, как режим чтения Chrome, голосовой поиск и даже перевод текста на более чем 100 языках без плагинов на вашем компьютере! Возьмите управление в свои руки с Google chrome - лучшим браузером для получения максимального удовольствия от работы в Интернете.", "feature_2_title": "Защитите свой компьютер\n", "feature_2_subtitle": " Защитите свой компьютер с помощью Google chrome. Благодаря таким функциям, как управление настройками безопасности, вы будете спокойны за свой компьютер, а ваши данные будут защищены.", "feature_3_title": "Ваш браузер заслуживает самого лучшего.\n", "feature_3_subtitle": " Chrome - самый эффективный и простой браузер для работы с новыми вкладками, навигации по закладкам или использования любимых расширений. С этим браузером вы можете делать все это, не загромождая рабочий стол и не разряжая аккумулятор.", "cta": "Это быстро, весело и бесплатно.\n", "button": " Скачать Google chrome"}, {"title": "Chrome - это веб-браузер для вас.\n", "subtitle": " Chrome - это лучший веб-браузер с необходимыми функциями и скоростью работы. Отлично подходит для работы, учебы или просто для просмотра веб-страниц.", "main_feature_title": "Сделайте свой просмотр более удобным.\n", "main_feature_subtitle": " Chrome разработан как быстрый, простой в использовании и безопасный браузер. В нем также есть десятки новых функций, которые делают работу в Интернете проще, чем когда-либо прежде.", "feature_1_title": "Повысьте свою производительность с помощью инструментов Google.\n", "feature_1_subtitle": " Инструменты Google позволяют работать умнее и эффективнее, поэтому вы сможете выполнять свою работу быстрее, чем когда-либо прежде. С помощью этих инструментов вы сможете сэкономить время на выполнение повседневных задач и повысить производительность труда в целом.", "feature_2_title": "Защитите свой веб-браузер и телефон\n", "feature_2_subtitle": " Chrome - лучший браузер для управления настройками безопасности в Интернете, что позволяет обеспечить безопасность аккаунта Google. С помощью нашего бесплатного браузера вы можете защитить свой ноутбук, телефон и планшет от вредоносных веб-сайтов.", "feature_3_title": "Ваш браузер - ваше время.\n", "feature_3_subtitle": " Постоянно пользуйтесь браузером Google chrome - это самый быстрый, простой и эффективный веб-браузер. Chrome также был создан для того, чтобы вы могли сосредоточиться на выполнении поставленной задачи, не отвлекаясь на посторонние дела. Быстрота и простота - вот что вам нужно от инструмента, который поможет вам добиться успеха в рабочих буднях.", "cta": "Этот браузер - лучший.\n", "button": " Получить Chrome"}]'
    return json.loads(text.replace("\n", ""))

if __name__ == '__main__':
    print("Не преминимо вне модуля")