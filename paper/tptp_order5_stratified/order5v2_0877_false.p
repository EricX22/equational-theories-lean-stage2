% order5v2_0877  eq1=22046 eq2=7974  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,Z)),f(Y,f(W,X))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(Z,f(f(Y,f(W,W)),X))) )).
