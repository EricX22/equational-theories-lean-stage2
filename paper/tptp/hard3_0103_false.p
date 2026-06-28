% hard3_0103  eq1=827 eq2=3332  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(f(X,Y),f(Y,Z))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(X,f(Z,f(Y,W))) )).
