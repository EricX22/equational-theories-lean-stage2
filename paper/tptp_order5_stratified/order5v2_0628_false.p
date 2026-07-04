% order5v2_0628  eq1=5360 eq2=59493  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(Z,f(Z,f(X,f(Y,Z))))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(f(X,Y),Y) != f(Y,f(f(Z,W),Y)) )).
