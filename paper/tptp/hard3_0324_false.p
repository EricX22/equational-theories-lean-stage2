% hard3_0324  eq1=3034 eq2=1228  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,W)),Z),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(X,f(f(f(X,Y),X),X)) )).
