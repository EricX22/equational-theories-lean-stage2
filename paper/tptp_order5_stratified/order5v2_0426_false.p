% order5v2_0426  eq1=36316 eq2=54897  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(X,X),Y),f(Z,W)),Z) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,f(Y,X)) != f(X,f(f(Y,X),X)) )).
