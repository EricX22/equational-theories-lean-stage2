% order5v2_0984  eq1=6720 eq2=1090  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(X,f(f(Y,Z),f(Z,W)))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(X,f(Y,Z)),Z)) )).
