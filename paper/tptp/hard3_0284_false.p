% hard3_0284  eq1=2678 eq2=3462  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(X,Y),f(Y,Z)),W) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,X) != f(X,f(f(Y,X),Y)) )).
