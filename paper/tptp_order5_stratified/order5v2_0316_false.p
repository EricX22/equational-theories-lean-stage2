% order5v2_0316  eq1=25158 eq2=50098  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(X,f(Z,X))),f(W,W)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(Z,f(Z,f(Y,X))),X) )).
