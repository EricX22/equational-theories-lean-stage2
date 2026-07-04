% order5v2_1815  eq1=10871 eq2=4729  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(f(X,f(Y,Z)),f(X,Z))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(X,f(X,f(Y,f(Y,f(Z,W))))) )).
