% order5_0058  eq1=27119 eq2=45051  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Y),f(Z,W)),f(U,X)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,X) != f(X,f(f(f(X,Y),Z),W)) )).
