% order5_0196  eq1=8802 eq2=7796  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(Z,f(f(f(Y,Y),X),X))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(Y,f(f(Z,f(Z,Z)),X))) )).
