% hard3_0092  eq1=707 eq2=4090  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(Y,f(Y,f(f(X,Y),Y))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,X) != f(f(f(Y,Y),X),X) )).
