from dataclasses import replace
import string

def dictionary(): #create dictionary, taking priority in reverse order
    d={}
    with open("dicts/eng_latn_us_broad.tsv") as f: #takes last listed pronunciation
        for line in f:
            fixedstring = line.replace(" ", "").replace("ˈ", "").replace("ː", "").replace("ˌ", "")
            (key, value) = fixedstring.split()
            d[key] = value
    with open("dicts/eng_latn_uk_broad.tsv") as f: #takes last listed pronunciation
        for line in f:
            fixedstring = line.replace(" ", "").replace("ˈ", "").replace("ː", "").replace("ˌ", "")
            (key, value) = fixedstring.split() 
            d[key] = value
    with open("dicts/cmudict.txt") as f:
        for line in f:
            fixedstring = line.split(",", 1)[0].lower().replace("ˈ", "").replace("ː", "").replace("ˌ", "") #takes first listed pronunciation
            (key, value) = fixedstring.split()
            d[key] = value
    return d

def transcribe(d):
    missedwords = {}
    
    wcount = 0
    prevwcount = 0
    with open("meta.txt", 'w') as meta:
        for i in range(15):
        
            missedbychap = {}
            filename = "chapters/dub_"
            if i < 9:
                filename += "0" + str(i+1)
            else:
                filename += str(i+1)
            with open(filename) as f:
                newfile = ""
                for line in f:
                    s = line.replace('-', '').split() #clean string
                    for n, i in enumerate(s):
                        wcount += 1
                        if i in d: #translate
                            s[n] = d[i]
                        else:
                            if i in missedwords:
                                missedwords[i] = (missedwords[i] + 1)
                            else:
                                missedwords[i] = 1
                            if i in missedbychap:
                                missedbychap[i] = (missedbychap[i] + 1)
                            else:
                                missedbychap[i] = 1
                    newfile += (' '.join(s) + '\n')
                    with open("trans" + filename + ".txt", "w") as f:
                        f.write(newfile)
                    meta.write("MISSED WORDS IN CHAPTER " + filename + " OUT OF " + str(wcount - prevwcount) + "\n")
                    uqword=0
                    totword=0
                    for k, v in missedbychap.items():
                        uqword += 1
                        totword += v
                    ratio = totword / (wcount - prevwcount)
                    prevwcount = wcount
                meta.write("%s/%s/%s \n" % (uqword, totword, ratio))

            with open("missedwords.txt", "w") as f: #count missed words
                otherkey = 0
                otherval = 0
                for k, v in missedwords.items():
                    if v < 5:
                        otherkey += 1
                        otherval += v
                    else: 
                        f.write('%s:%s\n' % (k, v))
                f.write('%s:%s\n' % (otherkey, otherval))

        meta.write("TOTAL WORD COUNT IS " + str(wcount))


d1 = dictionary()
transcribe(d1)