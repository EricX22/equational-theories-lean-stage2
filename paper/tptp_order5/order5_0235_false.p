% order5_0235  eq1=1576 eq2=25201  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(Y,f(Y,W))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,f(X,f(Z,W))),f(Y,Z)) )).
