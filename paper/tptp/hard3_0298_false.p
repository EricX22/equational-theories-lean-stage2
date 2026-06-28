% hard3_0298  eq1=2831 eq2=4385  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),f(W,Z)),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,f(X,X)) != f(f(Y,X),X) )).
