% hard3_0185  eq1=1661 eq2=3540  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,Y),f(f(Y,Z),Y)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(X,f(f(Z,W),X)) )).
