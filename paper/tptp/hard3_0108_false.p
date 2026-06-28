% hard3_0108  eq1=860 eq2=4316  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(f(Y,Z),f(Z,X))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,X)) != f(X,f(Z,X)) )).
