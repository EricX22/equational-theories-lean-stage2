% order5_0038  eq1=21115 eq2=54236  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(f(f(Y,W),X),Y)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,Y)) != f(Z,f(X,f(X,Y))) )).
