% order5_0173  eq1=44211 eq2=24697  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( f(X,X) = f(X,f(f(Y,f(Z,W)),U)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,Z),Z),f(f(Z,W),W)) )).
