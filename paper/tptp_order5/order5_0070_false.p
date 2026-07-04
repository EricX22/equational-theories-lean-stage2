% order5_0070  eq1=13416 eq2=19665  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,f(W,f(W,Z))),U)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(X,Y),f(f(X,f(X,Z)),W)) )).
