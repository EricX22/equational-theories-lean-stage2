% hard3_0385  eq1=4099 eq2=359  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,X) = f(f(f(Y,Y),Z),W) )).
fof(neg, negated_conjecture, ? [X] : ( f(X,X) != f(f(X,X),X) )).
