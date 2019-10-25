from lxml import html
from requests_html import HTMLSession


ENCODING_LINE = '<?xml version="1.0" encoding="utf-8"?>\n'
ODOO_TAG_LINE_OPEN = '<odoo noupdate="1">\n'
ODOO_TAG_LINE_CLOSE = '</odoo>'


def main():

    def get_value(obj):
        return ' '.join(obj[0].split()) if len(obj) else False

    session = HTMLSession()
    r = session.get('http://webinei.inei.gob.pe:8080/sisconcode/ubigeo/listaBusquedaUbigeoPorUbicacionGeografica.htm?versionCategoriaPK=5-1&nivel=1&strVersion=2016&strDpto=TODOS&strProv=TODOS&strDist=TODOS&flagDpto=&flagProv=&flagDist=http://webinei.inei.gob.pe:8080/sisconcode/ubigeo/listaBusquedaUbigeoPorUbicacionGeografica.htm?versionCategoriaPK=5-1&nivel=1&strVersion=2016&strDpto=TODOS&strProv=TODOS&strDist=TODOS&flagDpto=&flagProv=&flagDist=')
    tree = html.fromstring(r.content)

    trs = tree.xpath('/html/body/table[2]/tbody/tr')
    values = {}
    fs = open('res_country_state_data.xml', 'w')
    fp = open('l10n_pe_res_country_province_data.xml', 'w')
    fd = open('l10n_pe_res_country_district_data.xml', 'w')
    fs.write(ENCODING_LINE)
    fs.write(ODOO_TAG_LINE_OPEN)
    fp.write(ENCODING_LINE)
    fp.write(ODOO_TAG_LINE_OPEN)
    fd.write(ENCODING_LINE)
    fd.write(ODOO_TAG_LINE_OPEN)

    for tr in range(1, (len(trs) + 1)):
        depa = tree.xpath('/html/body/table[2]/tbody/tr[%s]/td[%s]/text()' % (tr, 2))
        prov = tree.xpath('/html/body/table[2]/tbody/tr[%s]/td[%s]/text()' % (tr, 3))
        dist = tree.xpath('/html/body/table[2]/tbody/tr[%s]/td[%s]/text()' % (tr, 4))

        codes, names = get_value(depa).split(' ', 1)
        codep, namep = get_value(prov).split(' ', 1)
        coded, named = get_value(dist).split(' ', 1)

        if get_value(dist):
            td = 4
            # print('%s %s %s' % (get_value(depa), get_value(prov), get_value(dist)))
            fd.write('<record id="l10n_pe_res_country_district_{}" model="l10n_pe.res.country.district"><field name="name">{}</field><field name="code">{}</field><field name="province_id" ref="l10n_pe_res_country_province_{}"/></record>\n'.format(coded, named, coded, codep))
        elif get_value(prov):
            td = 3
            # print('%s %s' % (get_value(depa), get_value(prov)))
            fd.write('<record id="l10n_pe_res_country_province_{}" model="l10n_pe.res.country.province"><field name="name">{}</field><field name="code">{}</field><field name="state_id" ref="res_country_state_{}"/></record>\n'.format(codep, namep, codep, codes))
        else:
            td = 2
            # print(get_value(depa))
            fd.write('<record id="res_country_state_{}" model="res.country.state"><field name="name">{}</field><field name="code">{}</field><field name="country_id" ref="base.pe"/></record>\n'.format(codes, names, codes))
            values[codes] = names

        try:
            tble_trs = tree.xpath('/html/body/table[2]/tbody/tr[%s]/td[%s]/div/table/tr' % (tr, td))
            ptable = {}
            for table_tr in range(1, (len(tble_trs) + 1)):
                key = False
                for i in [1, 3, 4, 6]:
                    temp = tree.xpath('/html/body/table[2]/tbody/tr[%s]/td[%s]/div/table/tr[%s]/td[%s]/text()' % (tr, td, table_tr, i))
                    temp = ' '.join(temp[0].split()) if len(temp) else ''
                    if key:
                        ptable[key] = temp
                        key = False
                    else:
                        key = temp
            # if len(ptable):
            # print(ptable)

        except Exception as esc:
            print(esc)
    # print(values)
    fs.write(ODOO_TAG_LINE_CLOSE)
    fp.write(ODOO_TAG_LINE_CLOSE)
    fd.write(ODOO_TAG_LINE_CLOSE)
    fs.close()
    fp.close()
    fd.close()


if __name__ == '__main__':
    main()
