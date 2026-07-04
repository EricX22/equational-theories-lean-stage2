% order5v2_1577  eq1=42373 eq2=4329  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( f(X,Y) = f(Z,f(W,f(U,f(X,U)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(Y,X)) != f(Z,f(X,W)) )).
