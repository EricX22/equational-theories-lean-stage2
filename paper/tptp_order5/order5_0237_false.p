% order5_0237  eq1=11138 eq2=48042  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(X,f(Z,Y)),f(Z,Z))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(Y,f(X,Z)),f(X,X)) )).
