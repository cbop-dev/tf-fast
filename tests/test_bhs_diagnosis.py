import sys
from tffast.tfData.tfBHS import TfBHS

tfBHS = TfBHS()
bnode = tfBHS.lookupBook("Deut")
canon = tfBHS.api.F.book.v(bnode)
node = tfBHS.getNodeFromBcV(canon, 1, 1)

print(f"Bnode: {bnode}, Canon: {canon}, Vnode: {node}")

# Simulate how main.py calls getLexemes2
res = tfBHS.getLexemes2(min=1, max=0, restrict=[], exclude=[], pos=True, sections=[node])
print(f"Total Words: {res.get('totalWords')}, Total Lexemes: {res.get('totalLexemes')}")
print(f"Lexemes: {res.get('lexemes')}")
