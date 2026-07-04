% order5_0035  eq1=34115 eq2=16115  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,Y),f(Z,f(W,X))),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(X,f(f(f(f(X,Y),X),Y),Y)) )).
