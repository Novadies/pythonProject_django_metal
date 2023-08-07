from .models import *
import csv
def zapis(reader):
    # try:
    #     reader = reader.chunks()
    #     fieldname = next(reader)
    #     print("ура "*100)
    # except Exception:
    reader = csv.DictReader(reader, delimiter=';')
    fieldname = list(reader.fieldnames)
    reader = list(reader)

    S = ["C", "Si", "Mn", "Cr", "Ni", "Ti", "Al", "W", "Mo", "Nb", "V", "S", "P", "Cu", "Co", "Zr", "Be", "Se", "N", "Pb", "Fe"]
    D = []
    def separation(data):
        data = data.strip()
        if data:
            t = '-'
            d = 'до'
            if t in data:
                data = data.split(t)
                if len(data) > 2: raise ValueError("Неверное разделение данных")
                data = [float(data[0]), float(data[1])]
            if d in data:
                data = data.split(t)
                if len(data) > 2: raise ValueError("Неверное разделение данных")
                data = [0.0 , float(data[1])]

            if type(data)==str : raise ValueError("Нет разбиения, неверные данные")
        else: data = [0.0 , 0.0]
        return data

    for i in reader:
        m = Metal()
        m_2 = Metal_2()
        for ss in S:
            for x in fieldname[1:-2]:
                if ss == x:
                    setattr(m, ss, str(i[x]))
                    if ss != "Fe":
                        setattr(m_2, locals()[f'{ss}_min'], separation(str(i[x]))[0])
                        setattr(m_2, locals()[f'{ss}_max'], separation(str(i[x]))[1])
                        m_2.save()
                        m.metal_compound=m_2

        mi = Metal_info(steel=i[fieldname[0]], steel_info=i[fieldname[-1]])
        m.metal_info=mi
        m.save()
        mi.save()

        data=i[fieldname[-2]].strip().capitalize()
        if data not in D:
            mc = Metal_class.objects.create(steel_class=data)
            mc.metals_info.add(mi)
            D.append(data)
        else:
            for num in D:
                if data == num:
                    mc = Metal_class.objects.get(steel_class=num)
                    mc.metals_info.add(mi)