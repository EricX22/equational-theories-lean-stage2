% order5v2_0387  eq1=32385 eq2=42470  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(Y,f(f(Y,f(Z,W)),U)),U) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,X) != f(Y,f(X,f(f(Y,X),Z))) )).
