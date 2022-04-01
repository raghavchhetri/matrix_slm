def move(step_um):
    positions=[]
    
# two choices: 0 or +step
    for j in range(512):
        a,b,c,d,e,f,g,h,i = f'{j:09b}'
        tmp=[step_um*int(a), step_um*int(b), step_um*int(c),
             step_um*int(d), step_um*int(e), step_um*int(f),
             step_um*int(g), step_um*int(h), step_um*int(i)]
        positions.append(tmp)

#two choices: 0 or -step
    for j in range(512):
        a,b,c,d,e,f,g,h,i = f'{j:09b}'
        tmp=[-step_um*int(a), -step_um*int(b), -step_um*int(c),
             -step_um*int(d), -step_um*int(e), -step_um*int(f),
             -step_um*int(g), -step_um*int(h), -step_um*int(i)]
        positions.append(tmp)

#two choices: +step or -step
    for j in range(512):
        a,b,c,d,e,f,g,h,i = f'{j:09b}'
        tmp=[step_um*int(a), step_um*int(b), step_um*int(c),
             step_um*int(d), step_um*int(e), step_um*int(f),
             step_um*int(g), step_um*int(h), step_um*int(i)]
        tmp = [-1*step_um if x == 0 else step_um for x in tmp]
        positions.append(tmp)
    
    return positions
    
if __name__ == '__main__':
    move()