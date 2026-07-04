% order5_0121  eq1=10989 eq2=34489  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(X,f(f(Y,f(Z,Y)),f(W,X))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(f(Y,Z),f(W,f(U,Z))),Y) )).
