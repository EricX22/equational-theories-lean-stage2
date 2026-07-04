% order5v2_0550  eq1=38895 eq2=29431  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,V,W,X,Y,Z] : ( X = f(f(f(Y,f(f(Z,W),U)),V),U) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(X,f(Y,f(Z,f(W,X)))),W) )).
