% hard3_0127  eq1=1014 eq2=4158  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,W),f(U,X))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(f(f(Y,X),Y),Y) )).
