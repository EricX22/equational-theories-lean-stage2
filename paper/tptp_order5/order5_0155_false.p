% order5_0155  eq1=6169 eq2=55835  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(Y,f(f(X,W),W)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(Y,X)) != f(f(Y,Z),f(W,Z)) )).
