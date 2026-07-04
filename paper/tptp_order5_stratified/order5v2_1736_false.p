% order5v2_1736  eq1=17689 eq2=14000  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(Z,f(W,f(Y,Y)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(Z,f(f(X,Y),W)),Y)) )).
