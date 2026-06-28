% hard3_0096  eq1=752 eq2=203  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(f(X,W),X))) )).
fof(neg, negated_conjecture, ? [X] : ( X != f(f(X,f(X,X)),X) )).
