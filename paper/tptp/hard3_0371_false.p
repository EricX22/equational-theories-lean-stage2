% hard3_0371  eq1=3705 eq2=4362  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,X) = f(f(Y,Z),f(Z,W)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,Z)) != f(Y,f(X,Z)) )).
