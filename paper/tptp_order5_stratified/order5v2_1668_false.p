% order5v2_1668  eq1=2309 eq2=17200  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(X,f(Y,Z))),W) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,X),f(X,f(Z,f(Y,X)))) )).
