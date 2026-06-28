% hard3_0055  eq1=363 eq2=4118  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,X) = f(f(X,Y),Z) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(f(f(X,X),X),Y) )).
