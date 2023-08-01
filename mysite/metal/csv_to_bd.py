from .models import Metal_info, Metal_class, Metal
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
    for i in reader:
        m = Metal()
        for ss in S:
            for x in fieldname[1:-2]:
                if ss == x:
                    setattr(m, ss, str(i[x]))
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