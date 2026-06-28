% hard3_0065  eq1=428 eq2=360  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(Y,f(X,f(X,Z)))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,X) != f(f(X,X),Y) )).
