% order5v2_1600  eq1=23743 eq2=60487  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),Y),f(Z,f(W,W))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(f(X,Y),Z) != f(f(X,Z),f(X,Z)) )).
