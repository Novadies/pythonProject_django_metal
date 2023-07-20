from .models import Metal_info, Metal_class, Metal
def zapis(reader):
    fieldname = list(reader.fieldnames)
    reader = list(reader)
    S = ["C", "Si", "Mn", "Cr", "Ni", "Ti", "Al", "W", "Mo", "Nb", "V", "S", "P", "Cu", "Co", "Zr", "Be", "Se", "N",
         "Pb", "Fe"]
    D = []
    for i in reader:
        m = Metal()
        for ss in S:
            for x in fieldname[1:-2]:
                if ss == x:
                    setattr(m, ss, str(i[x]))
        m.save()
        mi = Metal_info(steel=i[fieldname[0]], steel_info=i[fieldname[-1]])
        m.metal_info=mi
        mi.save()
        if i[fieldname[-2]] not in D:
            mc = Metal_class(steel_class=i[fieldname[-2]])
            mc.save()
            mc.metals_info.add(mi)
            D.append(i[fieldname[-2]])
        else:
            for num in D:
                if i[fieldname[-2]] == num:
                    mc = Metal_class.objects.get(steel_class=num)
                    mc.metals_info.add(mi)







