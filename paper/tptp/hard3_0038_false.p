% hard3_0038  eq1=207 eq2=3256  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,f(X,Y)),Z) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,X) != f(X,f(X,f(Y,Y))) )).
