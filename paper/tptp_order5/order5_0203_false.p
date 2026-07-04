% order5_0203  eq1=60399 eq2=52277  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(f(X,Y),Y) = f(f(Z,Y),f(Z,X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(f(X,f(X,Z)),X),Y) )).
