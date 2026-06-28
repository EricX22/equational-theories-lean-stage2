% hard3_0143  eq1=1096 eq2=476  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(X,f(Z,Y)),X)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(Y,f(X,f(Y,f(Y,X)))) )).
