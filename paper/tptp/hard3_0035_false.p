% hard3_0035  eq1=194 eq2=1075  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,Z),f(Z,X)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(Y,f(f(X,f(X,Y)),X)) )).
