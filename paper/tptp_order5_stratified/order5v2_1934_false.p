% order5v2_1934  eq1=32340 eq2=23644  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Y,f(Z,Y)),W)),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(Y,Z),X),f(Y,f(Z,Z))) )).
