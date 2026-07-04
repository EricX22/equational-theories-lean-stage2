% order5v2_1604  eq1=29934 eq2=30343  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,f(Z,f(Y,Y)))),W) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,f(X,f(f(X,Y),X))),Z) )).
