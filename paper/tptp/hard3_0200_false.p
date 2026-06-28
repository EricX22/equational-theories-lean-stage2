% hard3_0200  eq1=1845 eq2=1856  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,f(X,Y)),f(Z,Z)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(X,f(Y,X)),f(Z,W)) )).
