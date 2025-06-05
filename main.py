from os import remove
from time import time
from PIL import Image, ImageFont, ImageDraw
# from PIL.ImageEnhance import Color

width = 1100
height = 400

img = Image.new(mode="RGB", size=(width, height))
draw = ImageDraw.Draw(img)
fontSize = 32
# font = ImageFont.truetype("times.ttf", fontSize)
# font = ImageFont.truetype("Asana-Math.otf", fontSize)
font0 = ImageFont.truetype("fonts/latinmodern-math.otf", size=10)
font = ImageFont.truetype("fonts/latinmodern-math.otf", size=fontSize)
font1 = ImageFont.truetype("fonts/latinmodern-math.otf", size=int(fontSize/1.5))
fontSmall = ImageFont.truetype("fonts/latinmodern-math.otf", int(fontSize/2))

shift = 5
mathSights = ["+", "-", "/", "*", "=", "⋅", "·", "×", ":"]
mathSightsMultiply = ["*", "⋅", "·"]
eq_ = "y=(45^2+(((8)*2+(33/d-1))+66)/(2*(11 + (4:2)/2)*x - 99900))*8^(2+32/2)"
# eq_= "(1/1+3/(2+1))*8"
# eq_ = "2 + 3 ^ (4+8)"
# eq_="(1)/2-1"

eq = ""
for a in eq_:
    if a != " ":
        eq += a

def doBalance (eq_):
    eq = ""
    for a in eq_:
        if a == "*":
            eq += "·"
        elif a == ':':
            eq += "÷"
        else:
            eq += a

    return eq

eq = doBalance(eq)

def bracketsCheck (eq_):
    n = 0
    n2 = 0
    eq = ""
    for a in eq_:
        if a == "(": n += 1
        elif a == ")": n -= 1
        if a == "{": n2 += 1
        elif a == "}": n2 -= 1
        eq += a
        if n < 0:
            eq = "(" + eq
            n += 1
        if n2 < 0:
            eq = "{" + eq
            n2 += 1
    while n > 0:
        eq += ")"
        n -= 1
    while n2 > 0:
        eq += "}"
        n2 -= 1
    return eq

eq = bracketsCheck(eq)
print(eq)

def find_min (li):
    m : int = float('+inf')
    for a in li:
        if type(a) == list:
            m = min(m, find_min(a))
        else:
            m = min(m, a)
    return m

def find_max (li):
    m: int = float('-inf')
    for a in li:
        if type(a) == list:
            m = max(m, find_max(a))
        else:
            m = max(m, a)
    return m

def plusMinus (li, n):
    for a in range(len(li)):
        if type(li[a]) == list:
            li[a] = plusMinus(li[a], n)
        else:
            li[a] += n
    return li

def upReverseGo (l, li, wi):
    n = -find_min(li)
    wiEd = wiGetLast(wi)
    for i in reversed(range(len(l))):
        if l[i] in mathSights:
            break
        if type(l[i]) == list:
            li[i] = plusMinus(li[i], n+1)
            wiSt = wiGetFirst(wi[i])
        else:
            li[i] += 1
            wiSt = wi[i][0]
    return l, li, [wiSt, wiEd]

def downReverseGo (l, li, wi):
    div = False
    last = wiGetLast(wi)
    for i in reversed(range(len(l))):
        if div:
            if l[i] in mathSights:
                break
            elif type(wi[i][0]) == list:
                top = last - wiGetFirst(wi[i])
            else:
                top = last - wi[i][0]
        if l[i] == "/" and not div:
            n = -find_max(li[i:])
            bottom = last - wi[i][1]
            last = wi[i][1]
            div = True

    div = False
    if top > bottom:
        ch = False
        sub = abs(bottom + abs((top - bottom)) / 2)
    else:
        ch = True
        sub = top

    for i in reversed(range(len(l))):
        if div:
            if l[i] in mathSights:
                break
            elif type(wi[i][0]) == list:
                if ch:
                    wi[i] = plusMinus(wi[i], add)
                else:
                    wi[i] = plusMinus(wi[i], shift)
            else:
                if ch:
                    wi[i][0] += add
                else:
                    wi[i][0] += shift

        elif not div:
            if l[i] == "/":
                div = True
                if ch:
                    wi[i][0] += shift
                    wi[i][1] = wi[i][0] + bottom
                else:
                    wi[i][0] += shift
                    wi[i][1] += shift

                add = (bottom - top) / 2 + shift

            elif type(l[i]) == list:
                li[i] = plusMinus(li[i], n-1)
                wi[i] = plusMinus(wi[i], -sub + shift)
            else:
                li[i] -= 1
                wi[i][0] -= sub - shift
                if ch:
                    wi[i][1] -= top - shift*2
                else:
                    wi[i][1] -= bottom - shift*2

    if type(wi[-1][0]) == list:
        if ch:
            wi[-1] = wiSetLast(wi[-1], shift)
        else:
            wi[-1] = wiSetLast(wi[-1], (top - bottom)/2 + shift)
    return l, li, wi

def getMedian (st, ed):
    n = ed - st + 1
    if n % 2 == 1:
        return st + n // 2
    else:
        return st + n // 2 - 0.5

def bracketsInsert (l, li, wi, f):
    min = find_min(li)
    max = find_max(li)
    s = getMedian(min, max)
    s = 0
    if abs(min) + abs(max) > 3:
        l = ["⎛"] + ["⎝"] + l
        d = 0
        li = [s+0.5] + [s-2.5] + li
        f = [0] + [0] + f
        length = int(font.getlength("⎛"))
        wi = [[wi[0][0], length], [wi[0][0], length]] + plusMinus(wi, length)

        l += ["⎞"] + ["⎠"]
        li += [s+0.5] + [s-2.5]
        f += [0] + [0]
        length = int(font.getlength("⎞"))
        last = wiGetLast(wi)
        wi += [[last, last + length]] + [[last, last + length]]
    else:
        l = ["("] + l
        li = [s] + li
        f = [0] + f
        length = int(font.getlength("("))
        wi = [[wi[0][0], length]] + plusMinus(wi, length)

        l.append(")")
        li.append(s)
        f.append(0)
        length = int(font.getlength(")"))
        last = wiGetLast(wi)
        wi.append([last, last + length])

    return l, li, wi, f

def doPower (l, li, wi, f, start):
    for i in range(len(l)):
        if type(l[i]) == list:
            if i == 0:
                startIn = start
            else:
                startIn = wiGetLast(wi[:i])
            li[i], wi[i], f[i] = doPower(l[i], li[i], wi[i], f[i], startIn)
        else:
            li[i] += 0.4
            f[i] = 1
            if i == 0:
                wi[i][0] = start
            else:
                wi[i][0] = wi[i-1][1]
            wi[i][1] = wi[i][0] + font1.getlength(l[i])

    return li, wi, f

def doPowerGo (l, li, wi, f):
    for i in reversed(range(len(l))):
        if l[i] == "^":
            del l[i], li[i], wi[i], f[i]
            j = i
            break

    for i in range(j, len(l)):
        if type(l[i]) == list:
            start = wiGetLast(wi[:i])
            li[i], wi[i], f[i] = doPower(l[i], li[i], wi[i], f[i], start)
        else:
            li[i] += 0.4
            f[i] = 1
            wi[i][0] = wi[i-1][1]
            wi[i][1] = wi[i][0] + font1.getlength(l[i])

    return l, li, wi, f

def wiGetLast (wi):
    if wi == []:
        return 0
    if type(wi[-1][0]) == list:
        return wiGetLast(wi[-1])
    else:
        return wi[-1][1]

def wiSetLast (wi, n):
    if type(wi[-1][1]) == list:
        wi[-1] = wiSetLast(wi[-1], n)
    else:
        wi[-1][1] += n
    return wi

def wiGetFirst (wi):
    if wi == []:
        return 0
    elif type(wi[0][0]) == list:
        return wiGetFirst(wi[0])
    else:
        return wi[0][0]

def wiAppend (wi, length):
    if wi == []:
        wi.append([0, length])
    elif type(wi[-1][0]) == list:
        last = wiGetLast(wi[-1])
        wi.append([last, last + length])
    else:
        wi.append([wi[-1][1], wi[-1][1] + length])

    return wi

bracketOpen = ["(", "{"]
bracketClose = [")", "}"]

def getPosition (q):
    l = []  # Characters list
    li = [] # Height position list
    wi = [] # Width position list
    f = []  # Fonts list (for different size)
    i = 0
    mem = ""
    div = False
    power = False
    bracket = 0
    while True:
        b = q[i]
        if q[i] in bracketOpen:
            bracket += 1
            if bracket > 1:
                mem += q[i]
        elif q[i] in bracketClose and bracket > 1:
            bracket -= 1
            mem += q[i]
        elif q[i] in bracketClose and bracket == 1:
            bracket = 0
            l0, li0, wi0, f0 = getPosition(mem)
            if len(l) > 0 and l[-1] in mathSightsMultiply:
                l0, li0, wi0, f0 = bracketsInsert(l0, li0, wi0, f0)
            wi0 = plusMinus(wi0, wiGetLast(wi))
            l, li, wi, f = l+[l0], li+[li0], wi+[wi0], f+[f0]
            mem = ""
        elif bracket:
            mem += q[i]
        else:
            # Get height (partly width)
            if q[i] == "/":
                div = True
                l, li, swi = upReverseGo(l, li, wi)
            elif q[i] in mathSights and div:
                div = False
                l, li, wi = downReverseGo(l, li, wi)

            if q[i] in mathSightsMultiply and len(l) > 0 and type(l[-1]) == list and (l[-1][-1] != ")" and l[-1][-1] != "⎠"):
                l[-1], li[-1], wi[-1], f[-1] = bracketsInsert(l[-1], li[-1], wi[-1], f[-1])

            if q[i] == "^":
                power = True
            elif q[i] in mathSights and power:
                power = False
                l, li, wi, f = doPowerGo(l, li, wi, f)

            l.append(q[i])
            li.append(0)
            f.append(0)

            # Get width
            if q[i] == "/":
                wi.append(swi)
            else:
                symbolLength = int(font.getlength(q[i]))
                wi = wiAppend(wi, symbolLength)


        i += 1
        if i >= len(q):
            if div:
                l, li, wi = downReverseGo(l, li, wi)
            if power:
                l, li, wi, f = doPowerGo(l, li, wi, f)
            break
    return l, li, wi, f

start = time()
l, li, wi, f = getPosition(eq)
wi = plusMinus(wi, 10)
print(round((time() - start) * 10**3, 2))

print(l)
print(li)
print(wi)
print(f)

m = find_max(li)*fontSize/2+20
def doDraw (lR, liR, wiR, fR):
    # global w
    for a in range(len(lR)):
        # print(l[a] + "   " + str(li[a]))
        if type(liR[a]) == list:
            doDraw(lR[a], liR[a], wiR[a], fR[a])
        elif lR[a] == "/":
            y = -liR[a]*fontSize/2 + m + fontSize/2
            draw.line((wiR[a][0], y, wiR[a][1], y), fill=(255,255,255))
        else:
            fontUse = font0
            if fR[a] == 0:
                fontUse = font
            elif fR[a] == 1:
                fontUse = font1
            else:
                print("ERROR")
            draw.text((wiR[a][0], -liR[a]*fontSize/2 + m), lR[a], (255,255,255), font=fontUse)
            # draw.text((w, -liR[a]*25 + m), lR[a], (255,255,255), font=font)
            # w += int(font.getlength(str(lR[a])))
doDraw(l, li, wi, f)

draw.text((10, 250), eq, font=font)

# img.save("images/img.jpg")
img.show()