% order5v2_0398  eq1=42282 eq2=42060  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(Z,f(W,f(X,f(W,Z)))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(Z,f(X,f(Y,f(Z,Y)))) )).
