from fastapi.responses import FileResponse
from models import model

def getIndexPage():
    return FileResponse('views/public/index.html', media_type="text/html", status_code=200)

def createZip(data):
    try:
        folder = str(data['folder'])
        land = str(data['land'])
        link = model.createZip(folder, land)
        return {'status': 'ok', 'message': link}
    except Exception as err:
        print(err)
        return {'status': 'error', 'message': (f"Unexpected {err=}, {type(err)=}")}

def generateLand(data):
    """
    Валидация данных и отправка в модель
    """
    try:
        product_name = str(data['product_name']).strip()
        product_description = str(data['product_description']).strip()
        feature_1 = str(data['feature_1']).strip()
        feature_2 = str(data['feature_2']).strip()
        feature_3 = str(data['feature_3']).strip()
        if (len(product_name) < 3): raise Exception('Короткое "название продукта"')
        if (len(product_name) > 100): raise Exception('Длинное "название продукта"')
        if (len(product_description) < 20): raise Exception('Короткое "описание продукта"')
        if (len(product_description) > 600): raise Exception('Длинное "описание продукта"')
        if (len(feature_1) < 10): raise Exception('Короткая "особенность продукта 1"')
        if (len(feature_1) > 100): raise Exception('Длинная "особенность продукта 1"')
        if (len(feature_2) < 10): raise Exception('Короткая "особенность продукта 2"')
        if (len(feature_2) > 100): raise Exception('Длинная "особенность продукта 2"')
        if (len(feature_3) < 10): raise Exception('Короткая "особенность продукта 3"')
        if (len(feature_3) > 100): raise Exception('Длинная "особенность продукта 3"')
        validData = {}
        validData['product_name'] = product_name
        validData['product_description'] = product_description
        validData['feature_1'] = feature_1
        validData['feature_2'] = feature_2
        validData['feature_3'] = feature_3
        ["en","nl","fr","de","it","pl","es","pt-pt","pt-br","ru","ja","zh","bg","cs","da",
        "el","hu","lt","lv","ro","sk","sl","sv","fi","et"].index(str(data["language"]))
        ans = model.generateLand(validData, str(data["language"]))
        return {'status': 'ok', 'message': ans}
    except Exception as err:
        print(err)
        return {'status': 'error', 'message': (f"Ошибка: {err=}")}

if __name__ == '__main__':
    print("Не преминимо вне модуля")