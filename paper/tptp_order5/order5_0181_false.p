% order5_0181  eq1=42106 eq2=172  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( f(X,Y) = f(Z,f(X,f(W,f(U,Y)))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,X),f(Z,X)) )).
