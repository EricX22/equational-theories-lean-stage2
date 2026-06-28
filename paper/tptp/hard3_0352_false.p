% hard3_0352  eq1=3328 eq2=3313  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(X,f(Z,f(X,W))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(X,f(X,f(Z,Z))) )).
