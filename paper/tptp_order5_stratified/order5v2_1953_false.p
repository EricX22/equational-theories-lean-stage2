% order5v2_1953  eq1=18871 eq2=57373  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,Y),f(f(Z,Y),f(X,Y))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(X,Y)) != f(f(f(X,X),Z),X) )).
