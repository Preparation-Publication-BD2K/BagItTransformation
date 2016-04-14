import os

template = '''19\tCufflinks\ttranscript\t2997694\t3002576\t525\t-\t.\tgene_id "CUFF.1"; transcript_id "CUFF.1.1"; FPKM "11950.6967755138"; frac "0.163346"; conf_lo "9566.803651"; conf_hi "14384.618439"; cov "44.978057";\n'''

template2 = '''19\tCufflinks\texon\t2997694\t2997953\t525\t-\t.\tgene_id "CUFF.1"; transcript_id "CUFF.1.1"; exon_number "1"; FPKM "11950.6967755138"; frac "0.163346"; conf_lo "9566.803651"; conf_hi "14384.618439"; cov "44.978057";\n19\tCufflinks\texon\t3000645\t3000721\t525\t-\t.\tgene_id "CUFF.1"; transcript_id "CUFF.1.1"; exon_number "2"; FPKM "11950.6967755138"; frac "0.163346"; conf_lo "9566.803651"; conf_hi "14384.618439"; cov "44.978057";\n19\tCufflinks\texon\t3002351\t3002576\t525\t-\t.\tgene_id "CUFF.1"; transcript_id "CUFF.1.1"; exon_number "3"; FPKM "11950.6967755138"; frac "0.163346"; conf_lo "9566.803651"; conf_hi "14384.618439"; cov "44.978057";\n'''

filename = os.getcwd() + "/gene2medProbeExpr.txt"
with open(filename) as fn:
    lines = fn.readlines()
    cnt = 0
    files = []
    for line in lines:
        a = line.split('\t')
        if cnt == 0:
            for ls in range(1,len(a)):
                gtfname = a[ls] + ".gtf"
                files.append(gtfname)
                tmp = open(gtfname, "w")
                tmp.close()
        else:
            for ls in range(1, len(a)):
                gtfname = files[ls - 1]
                tmp = open(gtfname, "a")
                str1 = template.replace('"CUFF.1"', '"' + a[0] + '"')
                str2 = str1.replace("11950.6967755138", a[ls])
                tmp.write(str2)
                tmp.write(template2)
                tmp.close()
        cnt = cnt + 1

