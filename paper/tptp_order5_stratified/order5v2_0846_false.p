% order5v2_0846  eq1=53511 eq2=4418  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,V,W,X,Y,Z] : ( f(X,Y) = f(f(f(f(Z,X),W),U),V) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(X,Y)) != f(f(Z,X),W) )).
