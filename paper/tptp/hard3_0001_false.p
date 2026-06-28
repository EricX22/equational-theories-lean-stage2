% hard3_0001  eq1=5 eq2=625  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(Y,X) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(X,f(X,f(f(Y,Z),X))) )).
