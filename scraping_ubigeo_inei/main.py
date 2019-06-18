from lxml import html
from requests_html import HTMLSession


def main():

    def get_value(obj):
        return ' '.join(obj[0].split()) if len(obj) else False

    session = HTMLSession()
    r = session.get('http://webinei.inei.gob.pe:8080/sisconcode/ubigeo/listaBusquedaUbigeoPorUbicacionGeografica.htm?versionCategoriaPK=5-1&nivel=1&strVersion=2016&strDpto=TODOS&strProv=TODOS&strDist=TODOS&flagDpto=&flagProv=&flagDist=http://webinei.inei.gob.pe:8080/sisconcode/ubigeo/listaBusquedaUbigeoPorUbicacionGeografica.htm?versionCategoriaPK=5-1&nivel=1&strVersion=2016&strDpto=TODOS&strProv=TODOS&strDist=TODOS&flagDpto=&flagProv=&flagDist=')
    tree = html.fromstring(r.content)

    trs = tree.xpath('/html/body/table[2]/tbody/tr')
    values = {}
    for tr in range(1, (len(trs) + 1)):
        depa = tree.xpath('/html/body/table[2]/tbody/tr[%s]/td[%s]/text()' % (tr, 2))
        prov = tree.xpath('/html/body/table[2]/tbody/tr[%s]/td[%s]/text()' % (tr, 3))
        dist = tree.xpath('/html/body/table[2]/tbody/tr[%s]/td[%s]/text()' % (tr, 4))

        if get_value(dist):
            td = 4
            print('%s %s %s' % (get_value(depa), get_value(prov), get_value(dist)))
        elif get_value(prov):
            td = 3
            print('%s %s' % (get_value(depa), get_value(prov)))
        else:
            td = 2
            print(get_value(depa))
            code, value = get_value(depa).split(' ', 1)
            values[code] = value

        try:
            tble_trs = tree.xpath('/html/body/table[2]/tbody/tr[%s]/td[%s]/div/table/tr'% (tr, td))
            ptable = {}
            for table_tr in range(1, (len(tble_trs) + 1)):
                key = tree.xpath('/html/body/table[2]/tbody/tr[%s]/td[%s]/div/table/tr[%s]/td[1]/text()'% (tr, td, table_tr))
                value = tree.xpath('/html/body/table[2]/tbody/tr[%s]/td[%s]/div/table/tr[%s]/td[3]/text()'% (tr, td, table_tr))
                key = ' '.join(key[0].split()) if len(key) else ''
                value = ' '.join(value[0].split()) if len(value) else ''
                ptable[key] = value
            if len(ptable):
                print(ptable)

        except Exception as esc:
            print(esc)
    print(values)


if __name__ == '__main__':
    main()
