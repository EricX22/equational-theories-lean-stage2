% hard3_0138  eq1=1071 eq2=4631  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(X,f(f(Y,f(Z,W)),U)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(f(X,Y),X) != f(f(X,Z),X) )).
