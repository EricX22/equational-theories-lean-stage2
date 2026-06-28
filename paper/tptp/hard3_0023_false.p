% hard3_0023  eq1=110 eq2=10  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(f(Y,Z),X)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(X,f(Y,X)) )).
