import math, num2words, timeit, random

# common strings as values
def value_to_string(n="0"):
    vals = {0:"zero", 1:"one", 2:"two", 3:"three", 4:"four",
            5:"five", 6:"six", 7:"seven", 8:"eight", 9:"nine",
            # digits
            20:"twenty", 30:"thirty", 40:"forty", 50:"fifty",
            60:"sixty", 70:"seventy", 80:"eighty", 90:"ninety",
            # names tens units
            10:"ten", 11:"eleven", 12:"twelve", 13:"thirteen",
            14:"fourteen", 15:"fifteen", 16:"sixteen", 17:"seventeen",
            18:"eighteen", 19:"nineteen",
            # names teens
            }
    # if we have a trivial value
    if n in vals:
        # return it
        return vals[n]
    # or we have a mostly trivial value:
    if int(n) < 1000:
        n = int(n)
        out=""
        # remove any hundreds place
        if n > 99:
            out+=value_to_string(n // 100)+" hundred"
            n = n - 100*(n // 100)
            # and stop if we are done
            if n == 0:
                return out
        # check for additional trivial values
        if n < 20 or n%10 == 0:
            out+=" and "*(out!="")+vals[n]
            return out
        # otherwise, compute the tens stuff
        n = str(n)
        val = [int(n[x] + "0"*(len(n) - x - 1)) for x in range(len(n)) if n[x] != "0"]
        out += " and "*(len(out) > 0)
        out += "-".join([vals[int(x)] for x in val])
        return out
    # otherwise, figure out the representation
    return millions_to_string(n)

def millions_to_string(n=0):
    repl = {"tre":["s"], "se":["s", "x"], "septe":["m", "n"], "nove":["m", "n"]}
    millions = ["thousand", "mi", "bi", "tri", "quadri", "quinti", "sexti", "septi", "octi", "noni"]
    latin = {# units
             1:{1:["un",""], 2:["duo",""], 3:["tre",""], 4:["quattour",""], 5:["quinqua",""],
                6:["se",""], 7:["septe",""], 8:["octo",""], 9:["nove",""]},
             # tens
             10:{1:["deci","n"], 2:["viginti","ms"], 3:["triginta","ns"], 4:["quadraginta","ns"], 5:["quinquaginta","ns"],
                 6:["sexaginta","n"], 7:["septuaginta","n"], 8:["octoginta","mx"], 9:["nonaginta",""]},
             # hundreds
             100:{1:["centi","nx"], 2:["ducenti","n"], 3:["trecenti","ns"], 4:["quadringenti","ns"], 5:["quingenti","ns"],
                  6:["sescenti","n"], 7:["septingenti","n"], 8:["octingenti","mx"], 9:["nongenti",""]}}
    # compute the largest thousands power than encloses our value
    tpow = math.floor((len(str(n)) - 1) / 3) - 1
    number = int(n /  10**(3*tpow+3))
    # we need to change it up slightly if our key goes over 1000
    if tpow > 999:
        # fetch the number of millis needed
        millis = math.ceil(math.log(tpow, 1000))
        # now compute each power of ten
        temp=""
        #one billi trillion -> 2003 -> 10**6012 -> 2, 3
        for x in range(millis):
            # build from the lowest mill
            tpow, thispow = divmod(tpow, 1000)
            # fetch it's representation, changing zero for nil, one for blank, and "illion" for "illi"
            this = millions_to_string(10**(3 + 3 *thispow)).replace("zero", "nill").replace("one ", "").replace("illion", "illi")
            # and add it to the output
            temp = this + temp
        # and return the power of ten, adding the value to the front, and the final "illion"
        return value_to_string(number)+" "+temp+"on"
    # if we have a trivial solution
    if tpow < 10:
        # return it
        return value_to_string(number)+" "+millions[tpow]+"llion"*(tpow>0)
    # otherwise, decompose tpow into powers of ten
    tpow = str(tpow)
    tpow = [tpow[x] + "0"*(len(tpow) - x - 1) for x in range(len(tpow)) if tpow[x] != "0"]
    # itterate over tpow
    for x in tpow:
        # compute this position
        pos = tpow.index(x)
        # compute the power of ten this equates to
        pow = 10**(len(x)-1)
        # fetch the corresponding prefix
        pref = latin[pow][int(int(x) / pow)]
        # check if we need to change a unit prefix
        if pow == 1 and pref[0] in repl:
            # fetch the replacement type
            rep = tpow[pos-1][1]
            # check if we need to add anything
            for y in repl[pref[0]]:
                # if we do
                if y in rep:
                    # make the change
                    pref[0] += y
                    break
            tpow[pos] = pref
        else:
            # otherwise, just add the prefix
            tpow[pos] = pref
    # and deal with any words that change form due to those around them
    return "".join([value_to_string(number), " "] + [x[0] for x in tpow[::-1]] + ["llion"]).replace("ai", "i")

# common value strings
def value(n=""):
    vals = {"zero":0, "one":1, "two":2, "three":3, "four":4,
            "five":5, "six":6, "seven":7, "eight":8, "nine":9,
            # digits
            "twenty":20, "thirty":30, "forty":40, "fifty":50,
            "sixty":60, "seventy":70, "eighty":80, "ninety":90,
            # names tens units
            "eleven":11, "twelve":12, "thirteen":13, "fourteen":14,
            "fifteen":15, "sixteen":16, "seventeen":17, "eighteen":18,
            "nineteen":19,
            # names teens
            "hundred":100, "thousand":1000,
            # non-"illion" powers of ten
            }
    # if we have a trivial value
    if n in vals:
        # return it
        return vals[n]
    # otherwise, figure if it's a "-illion" power
    return millions(n)

# compute powers of ten in word
def millions(n=""):
    # only deal with "-illion"
    if "illion" not in n:
        return n
    # or if we have a XilliYilliZillion solution, we need to do something different
    illis = n.count("illi")
    if illis > 1:
        # split at the "illis"
        dif = [(x+"illion") for x in n.split("illi")[:-1]]
        # compute the power of a thousand
        dif = [round(math.log(millions(x), 1000)-1 if "nil" not in x else 0) for x in dif]
        # and convert to 1000000X + 1000Y + Z form
        dif = sum([dif[x] * 1000**(illis - x - 1) for x in range(illis)])
        # and return the power of ten
        return 10 ** (3 * dif + 3)
    out = 0
    # base prefixes
    latin = {# hundreds
              "centi":{"val":100, "pref":{"ses":6, "tre":3, "du":2, "":1}},
              "genti":{"val":100, "pref":{"non":9, "octin":8, "septin":7, "quin":5, "quadrin":4}},
              # tens
              "deci":{"val":10, "pref":{"":1}},
              "ginti":{"val":10, "pref":{"nona":9, "octo":8, "septua":7, "sexa":6, "quinqua":5, "quadra":4, "tri":3, "vi":2}},
              "ginta":{"val":10, "pref":{"nona":9, "octo":8, "septua":7, "sexa":6, "quinqua":5, "quadra":4, "tri":3}},
              # units
              "":{"val":1, "pref":{"nove":9, "octo":8, "septe":7, "sex":6, "quinqua":5, "quattuor":4, "tre":3, "duo":2, "un":1,
                                   # alternate units
                                   "non":9, "oct":8, "sept":7, "sext":6, "se":6, "quin":5, "quad":4, "tri":3, "bi":2, "mi":1, "ni":0}}}
    # itterate over the latinate words
    for x in latin:
        # if a latin is in the string
        if x in n:
            # fetch it
            p = latin[x]
            # and fetch any prefixes to the latinate
            pn = p["pref"]
            # itterate again
            for y in pn:
                # if they are joined correctly
                if y+x in n:
                    # add to the output
                    out += pn[y]*p["val"]
                    # and remove from the string
                    n = n.replace(y+x, "")
                    break
    # and return the power of ten as a number
    return 10**(3*out + 3) if out > 0 else 0

# convert a number to plain english
def num_to_string(n=0):
    # convert n to the integer and fractional values
    ints, fracs = (str(n)+".0").split(".")[:2]
    out=[]
    # if we have an integer section
    if ints != "0":
        # decompose ints into powers of 1000
        ints = decompose(int(ints), 1000)
        # compute the value of each grouping
        for x in ints:
            out.append(value_to_string(x))
        # add an "and" if the final integer value is under one hundred
        if len(out) > 1 and ints[-1] < 100:
            out[-1] = "and "+out[-1]
    else:
        out=["zero"]
    # comma seperation
    out = ", ".join(out)
    # if we have a fractional section
    if fracs != "0":
        # append a point, and add the values
        out += " ".join([" point"]+[value_to_string(x) for x in fracs])
    # and return the number'''
    return out.replace("allion", "illion").title()

# convert plain english to a number
def string_to_num(n="zero"):
    # split n into words
    n = n.lower().replace(",","").replace("-"," ").replace(" and ", " ").split(" ")
    # convert each of the words into their value
    n = [value(x) for x in n]
    # keep integers and fractions seperate
    m = []
    if "point" in n:
        n, m = n[:n.index("point")], n[n.index("point")+1:]
    # group by thousands
    a, out = 0, 0
    for x in range(len(n)):
        # if we hit a thousands value, or the end of the list
        if n[x] % 1000 == 0 or x==len(n)-1:
            # itterate on the found values
            for y in range(a, x):
                # if the current value is greater than the next
                if n[y] > n[y+1]:
                    # add them together
                    n[y+1] = n[y+1] + n[y]
                else:
                    # otherwise multiply them
                    n[y+1] = n[y+1] * n[y]
                # and remove the current value from n
                n[y] = 0
            # update the position of our pointer
            a = x+1
    # now do the fractional parts if any
    for x in range(len(m)):
        # they are a lot simpler
        n.append(float("0."+"0"*x+str(m[x])))
    # and return the constructed number
    return sum(n)

# decompose a number into powers of 1000
def decompose(num, pow=100, zerofrac=.2):
    # decompose using string manipulation
    def decompose_using_string(num, pow):
        # ensure num is a string, and change power to the 10th power
        num, pow = str(num), len(str(pow))-1
        tpow = pow*math.ceil(len(num) / pow)
        # pad the value so we have a length divisible by our power
        num = "0"*(tpow - len(num)) + num
        # and return the value as groups of thousands
        num = [int( num[x:(x+pow)] + "0"*(tpow - x - pow) ) for x in range(0, tpow, pow) if num[x:(x+pow)] != "0"*pow]
        return num
    # decompose using numerical manipulation
    def decompose_using_number(num, pow):
        # output list and power
        out = []
        # keep itterating until the number has been decomposed
        while num != 0:
            # compute the highest power to remove
            hpow = math.floor(math.log(num, pow))
            # remove that power from num, and fetch the power needed
            val, num = divmod(num, pow**hpow)
            # add that power to our output
            out.append(val*pow**hpow)
        return out
    # ensure pow is a power of ten
    pow = 10**round(math.log(pow, 10))
    # figure out if it's worth using string or number manipulation (string manip favours densely packed powers of 1000)
    if str(num).count("0") / len(str(num)) > zerofrac:
        # if the number is 25% zeroes, or more use numerical methods
        return decompose_using_number(num, pow)
    # otherwise use string manipulation
    return decompose_using_string(num, pow)

test_vals = ["three", "fourteen", "five hundred and sixty-seven", "zero point five zero nine three",
             "one trillion, nine hundred billion, five hundred and forty-six million, twenty-five thousand, and seven",
             "ninety", "three thousand, one hundred and forty-one point five nine",
             "sixty-five Ducentillion, thirteen Sexagintacentillion, four hundred and fifty-six quinquaquadragintillion, seventeen nonillion, and six",
             ]#"Three Milliquadrillion"]

# generate 100 random numbers whose length tends to increase
random_numbers = [random.randrange(100**x) for x in range(1, 10000)]
for num in random_numbers:
    times = 0
    print("----------------------------------------------------------------------")
    #print("the number is:", num)
    print()

    string = num_to_string(num)
    t1 = timeit.Timer(lambda: num_to_string(num)).timeit(times) / max(1, times)
    print("my code:")
    print(string)
    print("{:.9f}".format(t1), "seconds to execute")
    print()

    try:
        wordstring = num2words.num2words(num).title()
        t2 = timeit.Timer(lambda: num2words.num2words(num)).timeit(times) / max(1, times)
        print("num2words:")
        print(wordstring)
        print("{:.9f}".format(t2), "seconds to execute")
        print()
        print(wordstring == string)
        print("my code ran ", max(t1 / t2, t2 / t1), "times", "faster"*(t1 <= t2)+"slower"*(t2 < t1))
    except:
        wordstring = ""
    print("----------------------------------------------------------------------")
    print()

testvalues = ["Million", "Billion", "Trillion", "Quadrillion", "Quintillion", "Sextillion", "Septillion", "Octillion", "Nonillion", "Decillion", "Undecillion", "Duodecillion", "Tredecillion", "Quattuordecillion", "Quindecillion", "Sedecillion", "Septendecillion", "Octodecillion", "Novendecillion", "Vigintillion", "Unvigintillion", "Duovigintillion", "Tresvigintillion", "Quattuorvigintillion", "Quinvigintillion", "Sesvigintillion", "Septemvigintillion", "Octovigintillion", "Novemvigintillion", "Trigintillion", "Untrigintillion", "Duotrigintillion", "Trestrigintillion", "Quattuortrigintillion", "Quintrigintillion", "Sestrigintillion", "Septentrigintillion", "Octotrigintillion", "Noventrigintillion", "Quadragintillion", "Quinquagintillion", "Sexagintillion", "Septuagintillion", "Octogintillion", "Nonagintillion", "Centillion", "Uncentillion", "Decicentillion", "Undecicentillion", "Viginticentillion", "Unviginticentillion", "Trigintacentillion", "Quadragintacentillion", "Quinquagintacentillion", "Sexagintacentillion", "Septuagintacentillion", "Octogintacentillion", "Nonagintacentillion", "Ducentillion", "Trecentillion", "Quadringentillion", "Quingentillion", "Sescentillion", "Septingentillion", "Octingentillion", "Nongentillion", "Millinillion"]
