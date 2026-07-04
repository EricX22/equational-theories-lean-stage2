% order5_0091  eq1=42376 eq2=57788  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( f(X,Y) = f(Z,f(W,f(U,f(Y,Y)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(Y,Y)) != f(f(f(Z,Z),Z),W) )).
