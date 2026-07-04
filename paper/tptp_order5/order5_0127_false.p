% order5_0127  eq1=54237 eq2=59865  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,f(Y,Y)) = f(Z,f(X,f(X,Z))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(f(X,Y),Z) != f(W,f(f(Z,Y),W)) )).
