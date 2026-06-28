% hard3_0299  eq1=2841 eq2=4275  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),f(W,U)),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,f(X,X)) != f(Y,f(Y,X)) )).
