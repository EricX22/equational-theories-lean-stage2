% hard3_0248  eq1=2257 eq2=4583  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(X,f(Y,f(X,Y))),Y) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(f(X,X),X) != f(f(X,X),Y) )).
