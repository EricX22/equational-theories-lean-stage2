% order5v2_1324  eq1=39314 eq2=54468  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(f(Y,Y),f(Y,Z)),Y),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,Z)) != f(Z,f(X,f(X,Z))) )).
