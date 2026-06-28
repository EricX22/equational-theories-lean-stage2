% hard3_0235  eq1=2126 eq2=1071  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,Y),X),f(X,Z)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(X,f(f(Y,f(Z,W)),U)) )).
