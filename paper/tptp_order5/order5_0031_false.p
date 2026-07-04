% order5_0031  eq1=854 eq2=37959  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(f(Y,Z),f(X,Z))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,f(Z,f(W,W))),X),Y) )).
