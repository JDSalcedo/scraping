import requests
from lxml import html

URL = 'http://www.sunat.gob.pe/cl-ti-itmrconsruc'
URL_CAPTCHA = '/captcha'
URL_RUC = '/jcrS00Alias'


def main():
    sess = requests.Session()
    url_capcha = '%s%s' % (URL, URL_CAPTCHA)
    url_ruc = '%s%s' % (URL, URL_RUC)
    num_ruc = 20508565934
    try:
        resp_captcha = sess.post(url=url_capcha, data={"accion": "random"})
        # print('%s' % resp_captcha.text)
        resp_ruc = sess.post(
            url=url_ruc, data={"nroRuc": num_ruc, "accion": "consPorRuc",
                               "numRnd": resp_captcha.text}
        )
        # print('%s' % resp_ruc.content)
        tree = html.fromstring(resp_ruc.content)
        ruc = False
        name = tree.xpath('/html/body/table[1]/tr[1]/td[2]/text()')[0]
        if name.is_text:
            name = '%s' % name
            ruc, name = name.split(sep='-', maxsplit=1)
            name = ' '.join(name.split())
        rcomercial = tree.xpath('/html/body/table[1]/tr[3]/td[2]/text()')[0]
        street = tree.xpath('/html/body/table[1]/tr[7]/td[2]/text()')[0]
        if street.is_text:
            street = '%s' % street
            street = ' '.join(street.split())
        state = tree.xpath('/html/body/table[1]/tr[5]/td[2]/text()')[0]
        condition = tree.xpath('/html/body/table[1]/tr[6]/td[2]/text()')[0]
        if condition.is_text:
            # condition = condition.encode('utf-8').decode('utf-8')
            condition = '%s' % condition
            condition = ' '.join(condition.split())
        print(
            'Ruc: %s'
            '\nRazón Social: %s'
            '\nNombre comercial: %s'
            '\nDirección: %s'
            '\nEstado: %s'
            '\nCondición: %s'
            % (ruc, name, rcomercial, street, state, condition)
        )

    except Exception as exc:
        print('%s' % exc)


if __name__ == '__main__':
    main()
