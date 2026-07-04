% order5_0242  eq1=16596 eq2=56808  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(f(f(Y,Z),W),U),Y)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,Y)) != f(f(X,f(Y,Z)),X) )).
