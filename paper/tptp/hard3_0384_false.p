% hard3_0384  eq1=4088 eq2=3700  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,X) = f(f(f(Y,X),Z),Z) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,X) != f(f(Y,Z),f(Y,Z)) )).
