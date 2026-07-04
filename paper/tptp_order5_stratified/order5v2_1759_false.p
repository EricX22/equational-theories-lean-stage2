% order5v2_1759  eq1=16481 eq2=49860  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(f(f(Y,X),Z),Z),W)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(Y,f(Z,f(X,Z))),Z) )).
