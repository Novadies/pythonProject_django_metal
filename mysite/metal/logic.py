from .models import Metal
import re
def obrabotka():
    r1 = re.compile('-|—')
    r2 = re.compile('до')
    for M in Metal.objects.all():
        for i in Metal._S:
            data = getattr(M, i)
            result1 = r1.search(data)
            result1 = r2.search(data)
