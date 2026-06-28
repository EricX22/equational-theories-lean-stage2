% hard3_0146  eq1=1181 eq2=1429  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(Z,f(Z,X)),Y)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,X),f(X,f(Y,Y))) )).
