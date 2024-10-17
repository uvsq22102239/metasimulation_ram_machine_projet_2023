######################################### LIB #########################################

import ply.lex as lex
import ply.yacc as yacc

######################################### LEX #########################################

def main(path_ram:str) -> str:

    offset_if = []

    def formatage_if(ligne:str):
        offset_ligne = 0
        offset_del = 0
        for i in range(len(offset_if)):
            i -= offset_del
            offset_if[i] -= 1
            offset_ligne += 1
            if offset_if[i] == 0:
                offset_if.pop(i)
                offset_del += 1
        ligne = ("    " * offset_ligne) + ligne
        return ligne      
        

    def formatage_arguments(lencommand,tvalue) -> list:
        output = tvalue[lencommand+1:-1].split(',')
        for i, arg in enumerate(output):
            try:
                int(arg)
            except:
                if arg.find('@') >= 0:
                    r, rX = arg.split('@')
                    rX = "{"+f"r['{rX}']"+"}"
                    output[i] = f'r[f"{r}{rX}"]'
                else:
                    output[i] = f"r['{arg}']"
        return output


    tokens = ['LIGNE', 'ADD', 'MULT', 'DIV', 'MOD', 'WHILE', 'BREAK', 'IF']

    def t_ADD(t):
        r'ADD\(.+\)'
        t.value = formatage_arguments(3,t.value)
        t.value = f"{t.value[2]} = {t.value[0]} + {t.value[1]}\n"
        t.type = 'LIGNE'
        return t

    def t_MULT(t):
        r'MULT\(.+\)'
        t.value = formatage_arguments(4,t.value)
        t.value = f"{t.value[2]} = {t.value[0]} * {t.value[1]}\n"
        t.type = 'LIGNE'
        return t

    def t_SUB(t):
        r'SUB\(.+\)'
        t.value = formatage_arguments(3,t.value)
        t.value = f"{t.value[2]} = {t.value[0]} - {t.value[1]}\n"
        t.type = 'LIGNE'
        return t

    def t_DIV(t):
        r'DIV\(.+\)'
        t.value = formatage_arguments(3,t.value)
        t.value = f"{t.value[2]} = {t.value[0]} // {t.value[1]}\n"
        t.type = 'LIGNE'
        return t

    def t_MOD(t):
        r'MOD\(.+\)'
        t.value = formatage_arguments(3,t.value)
        t.value = f"{t.value[2]} = {t.value[0]} % {t.value[1]}\n"
        t.type = 'LIGNE'
        return t

    def t_JUMP(t):
        r'JUMP\(.+\)'
        t.value = formatage_arguments(4,t.value)
        if (v:=int(t.value[0])) < 0:
            t.type = 'WHILE'
            t.value = (v,"while True :\n")
        elif v > 0:
            t.type = 'BREAK'
            t.value = 'break\n'
        else:
            print("Illegal value for JUMP")
            t.lexer.skip(1)
        return t

    def t_JE(t):
        r'JE\(.+\)'
        t.value = formatage_arguments(2,t.value)
        if (v:=int(t.value[2])) < 0:
            t.type = 'WHILE'
            t.value = (v,f"while {t.value[0]} == {t.value[1]} :\n")
        elif v > 0:
            t.type = 'IF' # si les deux valeurs comparées sont différentes alors effectuer l'offset.
            t.value = (v,f"if {t.value[0]} != {t.value[1]} :\n")
        else:
            print("Illegal value for JE")
            t.lexer.skip(1)
        return t

    def t_JLT(t):
        r'JLT\(.+\)'
        t.value = formatage_arguments(3,t.value)
        if (v:=int(t.value[2])) < 0:
            t.type = 'WHILE'
            t.value = (v,f"while {t.value[0]} < {t.value[1]} :\n")
        elif v > 0:
            t.type = 'IF' # si t0 >= t1 alors effectuer l'offset.
            t.value = (v,f"if {t.value[0]} >= {t.value[1]} :\n")
        else:
            print("Illegal value for JLT")
            t.lexer.skip(1)
        return t

    def t_JGT(t):
        r'JGT\(.+\)'
        t.value = formatage_arguments(3,t.value)
        if (v:=int(t.value[2])) < 0:
            t.type = 'WHILE'
            t.value = (v,f"while {t.value[0]} > {t.value[1]} :\n")
        elif v > 0:
            t.type = 'IF' # si t0 >= t1 alors effectuer l'offset.
            t.value = (v,f"if {t.value[0]} <= {t.value[1]} :\n")
        else:
            print("Illegal value for JLT")
            t.lexer.skip(1)
        return t

    def t_error(t):
        if t.value[0] not in ['(',')',',','\n']:
            print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


    lexer = lex.lex()
    #with open("example.ram","r") as f:
    #    lexer.input("".join(f.readlines()))
    #    while (tok:=lexer.token()):
    #        print(tok)


    def p_code_ligne(p):
        '''code : LIGNE'''
        p[0] = [formatage_if(p[1])]

    def p_code_code_ligne(p):
        '''code : code LIGNE'''
        p[0] = p[1]+[formatage_if(p[2])]

    def p_code_code_WHILE(p):
        '''code : code WHILE'''
        lignes_code = p[1]
        v, value = p[2]
        value = formatage_if(value)
        codeBeforeWhile =  lignes_code[:v]
        codeInWhile = lignes_code[v:]
        for i, ligne in enumerate(codeInWhile):
            codeInWhile[i] = f"    {ligne}"
        p[0] = codeBeforeWhile + [value] + codeInWhile

    def p_code_code_IF(p):
        '''code : code IF'''
        v, value = p[2]
        value = formatage_if(value)
        offset_if.append(v)
        p[0] = p[1] + [value]

    # Error rule for syntax errors
    def p_error(p):
        print("Syntax error in input!")
        print(p)



    parser = yacc.yacc()
    with open(path_ram,"r") as f:
        resultat = parser.parse("".join(f.readlines()))
    resultat = "r = dict()\n" + "".join(resultat) + "print(r)"
    print(resultat)
    path_ram = path_ram.split('/')
    out_path = "/".join(path_ram[:-1] + [f"{path_ram[-1].split('.')[0]}.py"])
    with open(out_path,"w") as f:
        f.write(resultat)
    return out_path


if __name__ == '__main__':
    main("example.ram")