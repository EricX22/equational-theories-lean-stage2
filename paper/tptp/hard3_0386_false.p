% hard3_0386  eq1=4110 eq2=359  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,X) = f(f(f(Y,Z),Z),Z) )).
fof(neg, negated_conjecture, ? [X] : ( f(X,X) != f(f(X,X),X) )).
