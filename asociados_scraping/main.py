from lxml import html
from requests_html import HTMLSession


def main():
    session = HTMLSession()
    r = session.get('http://camaracusco.org/busqueda-letras.php')
    tree = html.fromstring(r.content)
    tables = tree.xpath('/html/body/table')
    for itable in range(2, len(tables) + 1):
        url_tr = '/html/body/table[%s]/tr' % (itable,)
        trs = tree.xpath(url_tr)
        for itr in range(1, len(trs) + 1):
            key = tree.xpath('%s[%s]/th[1]/text()' % (url_tr, itr))[0]
            td = '%s[%s]/td[1]/text()' if itr != 6 else '%s[%s]/td[1]/a/text()'
            lval = tree.xpath(td % (url_tr, itr))
            val = lval[0] if len(lval) > 0 else ''
            print('%s %s' % (key, val))
        print('')


if __name__ == '__main__':
    main()
