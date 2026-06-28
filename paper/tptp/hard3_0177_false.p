% hard3_0177  eq1=1573 eq2=3068  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,Z),f(Y,f(Y,X))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(f(X,Y),X),Y),X) )).
