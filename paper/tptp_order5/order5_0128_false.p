% order5_0128  eq1=31163 eq2=1642  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(X,f(f(Y,Z),f(Y,W))),W) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,X),f(f(Y,Z),Z)) )).
