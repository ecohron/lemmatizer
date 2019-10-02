from fststr import fststr
import pywrapfst as fst

class Lemmatizer:
    def __init__(self):
        self.st = fststr.symbols_table_from_alphabet(fststr.EN_SYMB)
        
        compiler = fst.Compiler(isymbols=self.st,osymbols=self.st,keep_isymbols=True,keep_osymbols=True)
        compiler.write('0 \n 0 0 <other> <other> \n0 0 <epsilon> <#>')
        preprocessFST = compiler.compile()
        fststr.expand_other_symbols(preprocessFST)
        
        self.inVocabFile = open("in_vocab_dictionary_verbs.txt")
        inVocabFST = self.getInVocabFST()
        morphoFST = self.getMorphoFST()
        alloFST = self.getAlloFST()

        compiler = fst.Compiler(isymbols=self.st,osymbols=self.st,keep_isymbols=True,keep_osymbols=True)
        compiler.write('\n0 \n0 0 <other> <other> \n0 1 <^> <epsilon> \n0 2 <#> +Guess \n1 1 <other> <epsilon> \n1 2 <#> +Guess \n2')
        oovPostFST = compiler.compile()
        fststr.expand_other_symbols(oovPostFST)
        temp = alloFST.union(oovPostFST)
        oovFST = fst.compose(morphoFST.arcsort(sort_type="olabel"), temp.arcsort(sort_type="ilabel"))
        oovFST = fst.compose(oovFST.arcsort(sort_type="olabel"), oovPostFST.arcsort(sort_type="ilabel"))
        self.fstOverall = fst.compose(preprocessFST.arcsort(sort_type="olabel"), inVocabFST.union(oovFST).arcsort(sort_type="ilabel"))
    
    def getInVocabFST(self):
        st = self.st
        compiler = fst.Compiler(isymbols=st,osymbols=st,keep_isymbols=True,keep_osymbols=True)
        compiler.write('')
        inVocabFST = compiler.compile()

        lineList = [line.rstrip('\n') for line in self.inVocabFile]
        for line in lineList:
            parts = line.split(',')
            parts[0] = [*parts[0]]
            parts[1] = [*parts[1]]
            for i in range(len(parts[0]) - len(parts[1])):
                parts[1].append('<epsilon>')
            for i in range(len(parts[1]) - len(parts[0])):
                parts[0].append('<epsilon>')
            fstword = ''
            for i in range(len(parts[0])):
                fstword += '\n' + str(i) + ' ' + str(i+1) + ' ' + parts[1][i] + ' ' + parts[0][i]
            fstword += '\n' + str(len(parts[0]) + 1)
            fstword += '\n' + str(len(parts[0])) + ' ' + str(len(parts[0])+1) + ' <#> +Known'
            ncompiler = fst.Compiler(isymbols=self.st,osymbols=self.st,keep_isymbols=True,keep_osymbols=True)
            ncompiler.write(fstword)
            fstNew = ncompiler.compile()
            fststr.expand_other_symbols(fstNew)
            inVocabFST.union(fstNew)
        
        fststr.expand_other_symbols(inVocabFST)
        return inVocabFST
    
    def getMorphoFST(self):
        compiler = fst.Compiler(isymbols=self.st,osymbols=self.st,keep_isymbols=True,keep_osymbols=True)
        compiler.write('')
        MorphoFST = compiler.compile()
        edFST = '\n0 0 <other> <other> \n0 1 e <epsilon> \n1 2 d <epsilon> \n1 0 <epsilon> e \n2 4 <#> <^> \n2 3 <epsilon> e \n3 0 <epsilon> d \n4 5 <epsilon> e \n5 6 <epsilon> d \n6 7 <epsilon> <#> \n7 \n7 7 <other> <other>'
        ingFST = '\n 0 0 <other> <other> \n0 1 i <epsilon> \n1 2 n <epsilon> \n1 0 <epsilon> i \n2 3 g <epsilon> \n2 9 <epsilon> i \n3 4 <#> <^> \n3 10 <epsilon> i \n4 5 <epsilon> i \n5 6 <epsilon> n \n6 7 <epsilon> g \n7 8 <epsilon> <#> \n8 \n8 8 <other> <other> \n9 0 <epsilon> n \n10 11 <epsilon> n \n11 0 <epsilon> g'
        sFST = '\n 0 0 <other> <other> \n0 1 s <epsilon> \n1 2 <#> <^> \n1 0 <epsilon> s \n2 3 <epsilon> s \n3 4 <epsilon> <#> \n4 \n4 4 <other> <other>'
        enFST = '\n0 0 <other> <other> \n0 1 e <epsilon> \n1 2 n <epsilon> \n1 0 <epsilon> e \n2 4 <#> <^> \n2 3 <epsilon> e \n3 0 <epsilon> n \n4 5 <epsilon> e \n5 6 <epsilon> n \n6 7 <epsilon> <#> \n7 \n7 7 <other> <other>'
        asIsFST = '\n0 1 <#> <^> \n0 0 <other> <other> \n1 2 <epsilon> <#> \n2 \n2 2 <other> <other>'
        
        edcompiler = fst.Compiler(isymbols=self.st,osymbols=self.st,keep_isymbols=True,keep_osymbols=True)
        edcompiler.write(edFST)
        edFSTNew = edcompiler.compile()
        fststr.expand_other_symbols(edFSTNew)
        
        ingcompiler = fst.Compiler(isymbols=self.st,osymbols=self.st,keep_isymbols=True,keep_osymbols=True)
        ingcompiler.write(ingFST)
        ingFSTNew = ingcompiler.compile()
        fststr.expand_other_symbols(ingFSTNew)
        
        scompiler = fst.Compiler(isymbols=self.st,osymbols=self.st,keep_isymbols=True,keep_osymbols=True)
        scompiler.write(sFST)
        sFSTNew = scompiler.compile()
        fststr.expand_other_symbols(sFSTNew)
        
        encompiler = fst.Compiler(isymbols=self.st,osymbols=self.st,keep_isymbols=True,keep_osymbols=True)
        encompiler.write(enFST)
        enFSTNew = encompiler.compile()
        fststr.expand_other_symbols(enFSTNew)
        
        asiscompiler = fst.Compiler(isymbols=self.st,osymbols=self.st,keep_isymbols=True,keep_osymbols=True)
        asiscompiler.write(asIsFST)
        asIsFSTNew = asiscompiler.compile()
        fststr.expand_other_symbols(asIsFSTNew)
        
        MorphoFST.union(edFSTNew.union(ingFSTNew.union(sFSTNew.union(enFSTNew.union(asIsFSTNew)))))
        fststr.expand_other_symbols(MorphoFST)
        return MorphoFST
    
    def getAlloFST(self):
        compiler = fst.Compiler(isymbols=self.st,osymbols=self.st,keep_isymbols=True,keep_osymbols=True)
        compiler.write('')
        AlloFST = compiler.compile()
        yRepl = '0 \n0 0 <other> <other> \n0 1 i <epsilon> \n1 2 e <epsilon> \n1 12 <^> <epsilon> \n1 0 <epsilon> i \n2 3 <^> <epsilon> \n2 9 <epsilon> i \n3 4 s <epsilon> \n3 10 <epsilon> i \n4 5 <#> y \n5 6 <epsilon> <^> \n6 7 <epsilon> s \n7 8 <epsilon> <#> \n8 \n8 8 <other> <other> \n9 0 <epsilon> e \n10 11 <epsilon> e \n11 0 <epsilon> <^> \n12 13 e <epsilon> \n12 19 <epsilon> i \n13 14 d <epsilon> \n13 20 <epsilon> i \n14 15 <#> y \n15 16 <epsilon> <^> \n16 17 <epsilon> e \n17 18 <epsilon> d \n18 8 <epsilon> <^> \n19 0 <epsilon> <^> \n20 21 <epsilon> <^> \n21 0 <epsilon> e'
        kIns = '\n0 \n0 0 <other> <other> \n0 1 c c \n1 0 <other> <other> \n1 2 k <epsilon> \n2 0 <epsilon> k \n2 3 <^> <epsilon> \n3 4 i <epsilon> \n 3 10 e <epsilon> \n3 14 <epsilon> k \n4 5 n <^> \n5 6 g i \n6 7 <#> n \n7 8 <epsilon> g \n8 9 <epsilon> <#> \n9 \n10 11 d <^> \n11 12 <#> e \n12 8 <epsilon> d \n14 0 <epsilon> <^>'
        eDel = '0 \n0 0 <other> <other> \n0 1 <^> <epsilon> \n1 2 i <epsilon> \n1 11 e <epsilon> \n2 3 n <epsilon> \n3 4 g <epsilon> \n4 5 <#> e \n5 6 <epsilon> <^> \n6 7 <epsilon> i \n7 8 <epsilon> n \n8 9 <epsilon> g \n9 10 <epsilon> <#> \n10 \n11 12 d <epsilon> \n11 16 <epsilon> e \n12 13 <#> e \n13 14 <epsilon> <^> \n14 15 <epsilon> e \n15 9 <epsilon> d \n16 0 <epsilon> <^>'
        eInsch = '0 \n0 0 <other> <other> \n0 1 c <epsilon> \n1 2 h <epsilon> \n1 0 <epsilon> c \n2 3 e <epsilon> \n2 11 <epsilon> c \n3 4 <^> <epsilon> '
        eInsch += '\n3 12 <epsilon> c \n4 5 s <epsilon> \n4 12 <epsilon> c \n5 6 <#> c \n6 7 <epsilon> h \n7 8 <epsilon> <^> \n8 9 <epsilon> s \n9 10 <epsilon> <#> \n10 \n10 10 <other> <other> \n11 0 <epsilon> h '
        eInsch += '\n12 13 <epsilon> h \n13 0 <epsilon> e \n14 15 <epsilon> h \n15 16 <epsilon> e \n16 0 <epsilon> <^>'
        eInss = '\n0 \n0 0 <other> <other> \n0 1 s <epsilon> \n1 2 e <epsilon> \n1 12 h <epsilon> \n1 0 <epsilon> s \n2 3 <^> <epsilon> \n2 9 <epsilon> s \n3 4 s <epsilon> \n3 10 <epsilon> s \n4 5 <#> s \n5 6 <epsilon> <^> \n6 7 <epsilon> s \n7 8 <epsilon> <#> \n8 \n8 8 <other> <other> \n9 0 <epsilon> e \n10 11 <epsilon> e \n11 0 <epsilon> <^> \n12 13 e <epsilon> \n 12 20 <epsilon> s \n13 14 <^> <epsilon> \n13 21 <epsilon> s \n14 15 s <epsilon> \n14 23 <epsilon> s \n15 16 <#> s \n16 17 <epsilon> h \n17 18 <epsilon> <^> \n18 19 <epsilon> s \n19 8 <epsilon> <#> \n20 0 <epsilon> h \n21 22 <epsilon> h \n22 0 <epsilon> e \n23 24 <epsilon> h \n24 25 <epsilon> e \n25 0 <epsilon> <^>'
        xz = [*'xz']
        eInsxz = '\n0 \n0 0 <other> <other> '
        for i in range(len(xz)):
            c = xz[i]
            n = 11*i
            eInsxz += '\n0 ' + str(n+1) + ' ' + c + ' <epsilon> ' + '\n' + str(n+1)  + ' ' + str(n+2) + ' e <epsilon> \n' + str(n+1) + ' 0 <epsilon> ' + c + '\n' + str(n+2)
            eInsxz += ' ' + str(n+3) + ' <^> <epsilon> \n' + str(n+2) + ' ' + str(n+9) + ' <epsilon> ' + c + ' \n' + str(n+3) +  ' ' + str(n+4) + ' s <epsilon> \n' + str(n+4)
            eInsxz += ' ' + str(n+5) + ' <#> ' + c + ' \n' + str(n+3) + ' ' + str(n+10) + ' <epsilon> ' + c + ' \n' + str(n+5) + ' ' + str(n+6) + ' <epsilon> <^> \n'
            eInsxz += str(n+6) + ' ' + str(n+7) + ' <epsilon> s \n' + str(n+7) + ' ' + str(n+8) + ' <epsilon> <#> \n' + str(n+8) + ' \n' + str(n+8) + ' ' + str(n+8) + ' <other> <other>'
            eInsxz += ' \n' + str(n+9) + ' 0 <epsilon> e \n' + str(n+10) + ' ' + str(n+11) + ' <epsilon> e \n' + str(n+11) + ' 0 <epsilon> <^>'
        compiler = fst.Compiler(isymbols=self.st,osymbols=self.st,keep_isymbols=True,keep_osymbols=True)
        compiler.write(eInsch)
        fstInsch = compiler.compile()
        fststr.expand_other_symbols(fstInsch)
        compiler = fst.Compiler(isymbols=self.st,osymbols=self.st,keep_isymbols=True,keep_osymbols=True)
        compiler.write(eInss)
        fstInss = compiler.compile()
        fststr.expand_other_symbols(fstInss)
        compiler = fst.Compiler(isymbols=self.st,osymbols=self.st,keep_isymbols=True,keep_osymbols=True)
        compiler.write(eInsxz)
        fstInsxz = compiler.compile()
        fststr.expand_other_symbols(fstInsxz)
        fsteIns = fstInsch.union(fstInss.union(fstInsxz))

        consonants = [*'bcdfghjklmnpqrstvwxz']
        consDoub = ''
        consDoub += '\n0 \n0 1 a a \n0 1 e e \n0 1 i i \n0 1 o o \n0 1 u u \n0 1 y y \n0 0 <other> <other>'
        consDoub += '\n1 0 a a \n1 0 e e \n1 0 i i \n1 0 o o \n1 0 u u \n1 0 y y'
        consDoub += '\n2 \n2 2 <other> <other>'
        for i in range(len(consonants)):
            c = consonants[i]
            consDoub += '\n1 ' + str(8*i + 3) + ' ' + c + ' ' + c
            consDoub += '\n' + str(8*i + 3) + ' ' + str(8*i + 4) + ' ' + c + ' <epsilon>'
            consDoub += '\n' + str(8*i + 3) + ' 0 <other> <other>'
            consDoub += '\n' + str(8*i + 4) + ' ' + str(8*i + 5) + ' <^> <^>'
            consDoub += '\n' + str(8*i + 5) + ' ' + str(8*i + 6) + ' i i'
            consDoub += '\n' + str(8*i + 5) + ' ' + str(8*i + 9) + ' e e'
            consDoub += '\n' + str(8*i + 5) + ' 0 <other> <other>'
            consDoub += '\n' + str(8*i + 6) + ' ' + str(8*i + 7) + ' n n'
            consDoub += '\n' + str(8*i + 7) + ' ' + str(8*i + 8) + ' g g'
            consDoub += '\n' + str(8*i + 8) + ' 2 <#> <#>'
            consDoub += '\n' + str(8*i + 9) + ' ' + str(8*i + 10) + ' d d'
            consDoub += '\n' + str(8*i + 9) + ' 0 <other> <other>'
            consDoub += '\n' + str(8*i + 10) + ' 2 <#> <#>'
        ycompiler = fst.Compiler(isymbols=self.st,osymbols=self.st,keep_isymbols=True,keep_osymbols=True)
        ycompiler.write(yRepl)
        yReplNew = ycompiler.compile()
        fststr.expand_other_symbols(yReplNew)
        
        kcompiler = fst.Compiler(isymbols=self.st,osymbols=self.st,keep_isymbols=True,keep_osymbols=True)
        kcompiler.write(kIns)
        kInsNew = kcompiler.compile()
        fststr.expand_other_symbols(kInsNew)
        
        edcompiler = fst.Compiler(isymbols=self.st,osymbols=self.st,keep_isymbols=True,keep_osymbols=True)
        edcompiler.write(eDel)
        eDelNew = edcompiler.compile()
        fststr.expand_other_symbols(eDelNew)
        
        cdcompiler = fst.Compiler(isymbols=self.st,osymbols=self.st,keep_isymbols=True,keep_osymbols=True)
        cdcompiler.write(consDoub)
        consDoubNew = cdcompiler.compile()
        fststr.expand_other_symbols(consDoubNew)

        AlloFST.union(yReplNew.union(kInsNew.union(fsteIns.union(eDelNew.union(consDoubNew)))))
        fststr.expand_other_symbols(AlloFST)
        return AlloFST

    def lemmatize(self, str):
        fststr.expand_other_symbols(self.fstOverall)
        return fststr.apply(str, self.fstOverall)

    def delemmatize(self, str):
        fststr.expand_other_symbols(self.fstOverall)
        toReturn = fststr.apply(str, self.fstOverall.invert())
        self.fstOverall.invert()
        return toReturn