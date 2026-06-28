% hard3_0058  eq1=373 eq2=359  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,X) = f(f(Y,Z),W) )).
fof(neg, negated_conjecture, ? [X] : ( f(X,X) != f(f(X,X),X) )).
