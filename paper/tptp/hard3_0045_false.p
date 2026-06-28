% hard3_0045  eq1=273 eq2=4362  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(f(Y,X),Y),X) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,Z)) != f(Y,f(X,Z)) )).
